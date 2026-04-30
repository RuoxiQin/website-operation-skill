---
name: blog-digest-html
description: Generates a beautiful, grid-based magazine style HTML digest from a list of blog articles. Use this when a task requires presenting articles, papers, or blog posts in an elegant, interactive HTML format.
---

# Blog Digest HTML Generation

This skill provides the exact specifications to generate a "Grid-based magazine style" HTML digest. It utilizes elegant serif typography, prominent headlines, high-contrast borders, and a warm paper-like background. 

Whenever you are asked to generate a magazine-style or grid-based HTML digest for a list of articles, apply the following design system.

## Design Specifications

### 1. Typography & Colors
- **Fonts**: Import `Playfair Display` (serif) for headings and `Lato` (sans-serif) for body text via Google Fonts.
- **Colors**:
  - Background: `#f4f1ea` (warm paper)
  - Main text: `#1a1a1a` (near black)
  - Secondary text: `#4a4a4a` (dark gray)
  - Accent: `#8b2b22` (deep red/burgundy)

### 2. Layout & Structure
- **Container**: Use a centered container (max-width: 1100px) bounded by a thick top border (4px) and bottom border (2px).
- **Masthead**: A centered header section with a large serif title (e.g., "The Issue" or "The Daily Digest") and an uppercase, letter-spaced date below it.
- **Grid Layout**: Articles must be placed in a CSS grid (`display: grid; grid-template-columns: 1fr 1fr; gap: 60px;`). For mobile screens (`max-width: 768px`), collapse to `1fr`.

### 3. Article Components
- **Category Tag**: Small, bold, uppercase text in the accent color, underlined with a 1px solid accent border.
- **Title**: Large serif text. Links should inherit the dark text color but transition to the accent color on hover.
- **Summary**: Clean, light-weight sans-serif text (`Lato`, 300 or 400 weight) with a generous line-height (e.g., `1.8`).
- **Read Button**: A transparent, outlined button (border uses main text color). On hover, it should invert (dark background, light text).

## Skeleton Template

Use this structure as the foundation for your generation:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Digest Title</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');
        
        /* Implement the colors, grid, and typography constraints here */
    </style>
</head>
<body>
    <div class="magazine-container">
        <header class="masthead">
            <h1>Publication Title</h1>
            <span class="issue-date">Date</span>
        </header>

        <div class="content-grid">
            <!-- Iterate over articles here -->
            <article class="article">
                <div><span class="article-category">Category</span></div>
                <h2 class="article-title"><a href="URL">Article Title</a></h2>
                <p class="article-summary">Article summary...</p>
                <a href="URL" class="read-btn">Read Full Story</a>
            </article>
        </div>
    </div>
</body>
</html>
```