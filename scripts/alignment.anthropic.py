"""
alignment.anthropic.py

A utility script to fetch and parse the Alignment Science Blog (https://alignment.anthropic.com/).
It extracts interpretability and alignment research notes, converting them 
into a clean Markdown list with absolute URLs.

Requires: beautifulsoup4

Usage:
    python3 scripts/alignment.anthropic.py [output_path]

If output_path is not provided, it defaults to .tmp/alignment_anthropic.md
"""

import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required libraries not installed. Please run 'pip install beautifulsoup4'")
    sys.exit(1)

def main():
    base_url = "https://alignment.anthropic.com/"
    output_path = sys.argv[1] if len(sys.argv) > 1 else ".tmp/alignment_anthropic.md"
    
    req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        print(f"Fetching {base_url}...")
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        print("Preprocessing HTML...")
        soup = BeautifulSoup(html, "html.parser")
        
        # The structure is somewhat similar to transformer circuits:
        # A list of <a> tags inside the main document body, sometimes with classes like 'note' or 'paper'.
        # We can extract them and clean them.
        
        markdown = "# Alignment Science Blog\n\nAnthropic's research notes on AI alignment.\n\n"
        
        # Check if they are grouped by dates (like transformer-circuits)
        toc = soup.find('div', class_='toc') or soup.find('body')
        
        if not toc:
            print("Could not find body or toc.")
            sys.exit(1)
            
        for element in toc.children:
            if element.name == 'div' and 'date' in element.get('class', []):
                date_text = element.get_text(strip=True)
                markdown += f"## {date_text}\n\n"
                
            elif element.name == 'a' and element.find('h3'):
                href = element.get('href', '')
                abs_href = urljoin(base_url, href)
                
                title_el = element.find('h3')
                title = title_el.get_text(strip=True) if title_el else ""
                
                byline_el = element.find('div', class_='byline')
                byline = byline_el.get_text(strip=True) if byline_el else ""
                
                desc_el = element.find('div', class_='description')
                desc = desc_el.get_text(strip=True) if desc_el else ""
                
                # Format: ### [Title](url)
                # **Byline** 
                # Description
                if title and abs_href:
                    markdown += f"### [{title}]({abs_href})\n\n"
                    if byline:
                        markdown += f"**{byline}**\n\n"
                    if desc:
                        # cleanup multi-line spaces
                        import re
                        desc = re.sub(r'\s+', ' ', desc)
                        markdown += f"{desc}\n\n"
                        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown.strip() + "\n")
            
        print(f"Successfully converted and stored in {output_path}")
        
    except Exception as e:
        print(f"Failed to fetch or convert the page: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
