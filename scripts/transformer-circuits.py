"""
transformer-circuits.py

A utility script to fetch and parse the Transformer Circuits Thread (https://transformer-circuits.pub).
It extracts papers, notes, and other interpretability resources, converting them 
into a clean Markdown list with absolute URLs.

Requires: beautifulsoup4

Usage:
    python3 scripts/transformer-circuits.py [output_path]

If output_path is not provided, it defaults to .tmp/transformer_circuits.md
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
    base_url = "https://transformer-circuits.pub"
    output_path = sys.argv[1] if len(sys.argv) > 1 else ".tmp/transformer_circuits.md"
    
    req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        print(f"Fetching {base_url}...")
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
        print("Preprocessing HTML...")
        soup = BeautifulSoup(html, "html.parser")
        
        toc = soup.find('div', class_='toc')
        if not toc:
            print("Could not find the table of contents.")
            sys.exit(1)
            
        markdown = "# Transformer Circuits Thread\n\nAnthropic's mechanistic interpretability research.\n\n"
        
        for element in toc.children:
            if element.name == 'div' and 'date' in element.get('class', []):
                date_text = element.get_text(strip=True)
                markdown += f"## {date_text}\n\n"
                
            elif element.name == 'a':
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
                        markdown += f"{desc}\n\n"
                        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown.strip() + "\n")
            
        print(f"Successfully converted and stored in {output_path}")
        
    except Exception as e:
        print(f"Failed to fetch or convert the page: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
