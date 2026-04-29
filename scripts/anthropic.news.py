"""
anthropic.news.py

A utility script to fetch and parse the Anthropic Newsroom (https://www.anthropic.com/news).
It cleans up the HTML by removing images and SVGs, correctly formats nested Markdown headings 
inside anchor tags, and converts all relative links into absolute URLs. 
The cleaned content is then converted to Markdown and saved to a file.

Requires: beautifulsoup4, markdownify

Usage:
    python3 scripts/anthropic.news.py [output_path]

If output_path is not provided, it defaults to .tmp/anthropic_news.md
"""

import urllib.request
from urllib.parse import urljoin
import sys
import re

try:
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md
except ImportError:
    print("Error: Required libraries not installed. Please run 'pip install beautifulsoup4 markdownify'")
    sys.exit(1)

def main():
    base_url = "https://www.anthropic.com"
    url = f"{base_url}/news"
    output_path = sys.argv[1] if len(sys.argv) > 1 else ".tmp/anthropic_news.md"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        print(f"Fetching {url}...")
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        print("Preprocessing HTML...")
        soup = BeautifulSoup(html, "html.parser")
        
        # 1. Remove all images, svgs, and videos
        for tag in soup.find_all(['img', 'svg', 'picture', 'video', 'canvas', 'iframe']):
            tag.decompose()
            
        # 2. Convert all relative URLs to absolute URLs
        for a in soup.find_all('a'):
            href = a.get('href')
            if href:
                a['href'] = urljoin(base_url, href)

        # 2.5 Convert specific span tags to h4 to ensure they are extracted correctly
        for span in soup.find_all('span', class_=re.compile(r'title', re.I)):
            span.name = 'h4'
            
        # Also add spaces around time tags to prevent them from sticking to other text
        for time_tag in soup.find_all('time'):
            time_tag.insert_before(' ')
            time_tag.insert_after(' ')

        # 3. Fix block-level elements inside 'a' tags for cleaner markdown
        for a in soup.find_all('a'):
            headings = a.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])
            if headings:
                href = a.get('href', '')
                for h in headings:
                    new_a = soup.new_tag('a', href=href)
                    for content in list(h.contents):
                        new_a.append(content)
                    h.clear()
                    h.append(new_a)
                
                a.name = 'div'
                if 'href' in a.attrs:
                    del a['href']
        
        cleaned_html = str(soup)
        
        print("Converting to markdown...")
        markdown_content = md(cleaned_html, heading_style="ATX", escape_asterisks=False, escape_underscores=False)
        
        # Clean up multiple blank lines
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content.strip() + "\n")
            
        print(f"Successfully converted and stored in {output_path}")
        
    except Exception as e:
        print(f"Failed to fetch or convert the page: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
