"""
claude.blog.py

A utility script to fetch and parse the Claude Blog (https://claude.com/blog).
Since the Claude website uses complex marketing grids, duplicated lists, and
screen-reader-only elements that translate poorly to raw Markdown, this script
extracts the semantic information directly from the DOM and constructs a clean
Markdown index of the blog categories and recent posts.

Requires: beautifulsoup4

Usage:
    python3 scripts/claude.blog.py [output_path]

If output_path is not provided, it defaults to .tmp/claude_blog.md
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
    base_url = "https://claude.com"
    url = f"{base_url}/blog"
    output_path = sys.argv[1] if len(sys.argv) > 1 else ".tmp/claude_blog.md"
    
    try:
        current_url = url
        items = []
        unique_cats = []
        seen_cats = set()
        
        while current_url:
            print(f"Fetching {current_url}...")
            req = urllib.request.Request(current_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                html = response.read().decode('utf-8')
                
            soup = BeautifulSoup(html, "html.parser")
            
            # Extract blog items and add to our cumulative list
            items.extend(soup.find_all('div', class_='blog_cms_item'))
            
            # Extract category links (only needed from the first page, but deduped anyway)
            for cat in soup.find_all('a', href=lambda href: href and '/blog/category/' in href):
                name, link = cat.text.strip(), urljoin(base_url, cat.get('href'))
                if link not in seen_cats and name:
                    seen_cats.add(link)
                    unique_cats.append((name, link))
                    
            # Check for the "View more" next page link
            next_button = soup.find('a', class_='w-pagination-next')
            if next_button and next_button.get('href'):
                current_url = urljoin(url, next_button.get('href'))
            else:
                current_url = None
                
        print("Extracting blog metadata and posts...")
                
        # Build the final markdown string
        markdown = "# Claude Blog\n\nProduct news and best practices for teams building with Claude.\n\n"
        
        if unique_cats:
            markdown += "## Categories\n"
            for name, link in unique_cats:
                markdown += f"- [{name}]({link})\n"
            markdown += "\n"
            
        markdown += "## Latest Posts\n\n"
        
        # De-duplicate posts because sometimes they show up twice in the DOM (e.g. grid vs list view)
        seen_links = set()
        
        for item in items:
            title_div = item.find('div', class_=lambda c: c and 'card_blog_title' in c)
            title = title_div.text.strip() if title_div else None
            
            date_div = item.find('div', attrs={"fs-list-field": "date"})
            if not date_div:
                 # fallback for grid date
                 date_div = item.find('div', class_=lambda c: c and 'u-text-style-caption' in c and 'u-foreground-tertiary' in c)
            date = date_div.text.strip() if date_div else ""
            
            cat_div = item.find('div', attrs={"fs-list-field": "category"})
            category = cat_div.text.strip() if cat_div else ""
            
            link_a = item.find('a', class_='clickable_link')
            if not link_a:
                 # fallback link
                 link_a = item.find('a', attrs={"fs-list-element": "item-link"})
            href = link_a.get('href') if link_a else ""
            abs_href = urljoin(base_url, href) if href and href != "#" else ""
            
            if not title or not abs_href or abs_href in seen_links:
                continue
                
            seen_links.add(abs_href)
            
            markdown += f"### [{title}]({abs_href})\n"
            if category or date:
                markdown += f"**{category}** • {date}\n\n"
            else:
                markdown += "\n"
            
        print("Converting to markdown...")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)
            
        print(f"Successfully converted and stored in {output_path}")
        
    except Exception as e:
        print(f"Failed to fetch or convert the page: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
