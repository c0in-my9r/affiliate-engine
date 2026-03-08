from pathlib import Path

keywords_file = "keywords.csv"
content_dir = Path("content/tools")
content_dir.mkdir(parents=True, exist_ok=True)

with open(keywords_file, "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f if line.strip()]

for keyword in keywords:
    slug = keyword.lower().replace("&", "and")
    slug = "".join(c if c.isalnum() or c == " " else "" for c in slug)
    slug = "-".join(slug.split())

    filepath = content_dir / f"{slug}.md"
    title = keyword.title()
    description = f"Discover the best AI tools for {keyword}."

    body = f"""---
title: "{title}"
date: 2026-03-08T09:30:00Z
draft: false
description: "{description}"
---

# {title}

This page covers the best AI tools for **{keyword}**.

## What you'll find here

- Useful AI tools for this use case
- What each tool does well
- Which options are best for beginners, pros, and budgets

## Recommended starting points

This section will later be expanded with tool comparisons, pricing, pros and cons, and affiliate links.
"""

    with open(filepath, "w", encoding="utf-8") as out:
        out.write(body)

print(f"Done. Generated {len(keywords)} pages in {content_dir}/")
