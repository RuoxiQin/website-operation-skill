"""
anthropic.economic-futures.py

A utility script to fetch and parse the Anthropic Economic Futures blog (https://www.anthropic.com/economic-futures).
It cleans up the HTML by removing images and SVGs, correctly formats nested Markdown headings
inside anchor tags, and converts all relative links into absolute URLs.
The cleaned content is then converted to Markdown and saved to a file.

Requires: beautifulsoup4, markdownify, playwright
  pip install beautifulsoup4 markdownify playwright
  playwright install chromium

Usage:
    python3 scripts/anthropic.economic-futures.py [output_path]

If output_path is not provided, it defaults to .tmp/anthropic_economic_futures.md
"""

from fetch import fetch_html
from urllib.parse import urljoin
import sys

try:
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md
except ImportError:
    print("Error: Required libraries not installed. Please run 'pip install beautifulsoup4 markdownify'")
    sys.exit(1)

def main():
    base_url = "https://www.anthropic.com"
    url = f"{base_url}/economic-futures"
    output_path = sys.argv[1] if len(sys.argv) > 1 else ".tmp/anthropic_economic_futures.md"

    try:
        print(f"Fetching {url}...")
        html = fetch_html(url)
            
        print("Preprocessing HTML...")
        soup = BeautifulSoup(html, "html.parser")
        
        # 1. Remove all images and SVGs
        for img in soup.find_all(['img', 'svg', 'picture']):
            img.decompose()
            
        # 2. Add spaces after inline elements for better readability in markdown
        for el in soup.find_all(['time', 'span']):
            if el.string:
                el.string.replace_with(el.string + ' ')
                
        # Remove list header which just says "Date Category Title"
        for header in soup.find_all('div', class_=lambda c: c and 'listHeader' in c):
            header.decompose()
            
        # Remove screen-reader only elements (e.g. "Search")
        for sr in soup.find_all(class_=lambda c: c and ('srOnly' in c or 'sr-only' in c)):
            sr.decompose()
            
        # Parse publication list items cleanly into headings
        for a in soup.find_all('a', class_=lambda c: c and 'listItem' in c):
            title_span = a.find('span', class_=lambda c: c and 'title' in c)
            if title_span:
                title = title_span.get_text(strip=True)
                href = a.get('href', '')
                
                date_time = a.find('time')
                cat_span = a.find('span', class_=lambda c: c and 'subject' in c)
                
                date = date_time.get_text(strip=True) if date_time else ""
                cat = cat_span.get_text(strip=True) if cat_span else ""
                
                # Build replacement DOM
                container = soup.new_tag('div')
                
                h3 = soup.new_tag('h3')
                new_a = soup.new_tag('a', href=href)
                new_a.string = title
                h3.append(new_a)
                container.append(h3)
                
                if cat or date:
                    meta = soup.new_tag('p')
                    if cat:
                        b = soup.new_tag('strong')
                        b.string = cat
                        meta.append(b)
                    if cat and date:
                        meta.append(" • ")
                    if date:
                        meta.append(date)
                    container.append(meta)
                    
                if a.parent and a.parent.name == 'li':
                    a.parent.replace_with(container)
                else:
                    a.replace_with(container)

        # 3. Convert all relative URLs to absolute URLs
        for a in soup.find_all('a'):
            href = a.get('href')
            if href:
                a['href'] = urljoin(base_url, href)

        # 4. Fix block-level elements inside 'a' tags for cleaner markdown
        for a in soup.find_all('a'):
            headings = a.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
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
        markdown_content = md(cleaned_html, heading_style="ATX")
        
        # Clean up multiple blank lines
        import re
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content.strip() + "\n")
            
        print(f"Successfully converted and stored in {output_path}")
        
    except Exception as e:
        print(f"Failed to fetch or convert the page: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
