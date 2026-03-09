#!/usr/bin/env python3

import csv
import os
import re
from pathlib import Path

KEYWORDS_FILE = "keywords.csv"
OUTPUT_DIR = Path("content/tools")
DATE = "2026-03-08T09:30:00Z"


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def title_case(text: str) -> str:
    small_words = {"for", "and", "or", "the", "a", "an", "to", "of", "in", "on", "with"}
    words = text.split()
    titled = []
    for i, word in enumerate(words):
        if i != 0 and i != len(words) - 1 and word.lower() in small_words:
            titled.append(word.lower())
        else:
            titled.append(word.capitalize())
    return " ".join(titled)


def normalize_topic(keyword: str) -> str:
    k = keyword.strip().lower()

    prefixes = [
        "best ai tools for ",
        "ai tools for ",
        "best tools for ",
        "tools for ",
    ]
    for prefix in prefixes:
        if k.startswith(prefix):
            k = k[len(prefix):]
            break

    replacements = {
        "seo": "SEO",
        "tiktok": "TikTok",
        "youtube": "YouTube",
        "shopify": "Shopify",
        "ecommerce": "eCommerce",
        "email": "email",
        "note taking": "note-taking",
        "small business": "small businesses",
        "local businesses": "local businesses",
        "product managers": "product managers",
        "virtual assistants": "virtual assistants",
        "research papers": "research papers",
        "graphic design": "graphic design",
        "interior design": "interior design",
        "lead generation": "lead generation",
        "project management": "project management",
        "social media": "social media",
        "content creation": "content creation",
        "customer service": "customer service",
        "blog writing": "blog writing",
        "podcast editing": "podcast editing",
        "video editing": "video editing",
        "keyword research": "keyword research",
        "real estate": "real estate",
    }

    if k in replacements:
        return replacements[k]

    return k


def page_title_from_topic(topic: str) -> str:
    special = {
        "SEO": "Best AI Tools for SEO",
        "TikTok": "Best AI Tools for TikTok",
        "YouTube": "Best AI Tools for YouTube",
        "Shopify": "Best AI Tools for Shopify",
        "eCommerce": "Best AI Tools for eCommerce",
    }
    if topic in special:
        return special[topic]
    return f"Best AI Tools for {title_case(topic)}"


def meta_description(topic: str) -> str:
    return f"Discover the best AI tools for {topic}, including beginner-friendly picks, workflow options, and practical starting points."


def intro_paragraph(topic: str) -> str:
    return (
        f"Looking for the best AI tools for {topic}? This guide is designed to help you quickly identify "
        f"useful options based on workflow, skill level, and budget."
    )


def who_this_is_for(topic: str) -> str:
    return (
        f"This page is for people exploring AI tools for {topic}, whether you want a simple starting point, "
        f"a faster workflow, or a more advanced stack."
    )


def starter_bullets(topic: str):
    return [
        f"Tools that can save time in {topic}",
        f"Options for beginners, pros, and budget-conscious users",
        f"Practical categories to compare before choosing a tool",
    ]


def comparison_bullets(topic: str):
    return [
        "Ease of use and learning curve",
        "Output quality and reliability",
        "Pricing, free plans, and upgrade paths",
        f"Whether the tool fits your {topic} workflow",
    ]


def body_for_keyword(keyword: str) -> str:
    topic = normalize_topic(keyword)
    page_title = page_title_from_topic(topic)
    description = meta_description(topic)
    slug = slugify(keyword)

    starter_lines = "\n".join([f"- {item}" for item in starter_bullets(topic)])
    compare_lines = "\n".join([f"- {item}" for item in comparison_bullets(topic)])

    body = f"""---
title: "{page_title}"
date: {DATE}
draft: false
description: "{description}"
---

## Overview

{intro_paragraph(topic)}

{who_this_is_for(topic)}

## What you'll find here

{starter_lines}

## What to compare before choosing

{compare_lines}

## Recommended starting points

A strong next version of this page should include specific tool recommendations, quick comparisons, pricing notes, and affiliate links where relevant.

## Related guides

- [Browse all AI tool guides](/tools/)
"""
    return slug, body


def read_keywords():
    keywords = []
    with open(KEYWORDS_FILE, newline="", encoding="utf-8") as f:
        sample = f.read(2048)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample) if "," in sample else csv.excel
        reader = csv.reader(f, dialect)

        for row in reader:
            if not row:
                continue
            keyword = row[0].strip()
            if not keyword:
                continue
            if keyword.lower() == "keyword":
                continue
            keywords.append(keyword)

    return keywords


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for old_file in OUTPUT_DIR.glob("*.md"):
        old_file.unlink()

    keywords = read_keywords()

    for keyword in keywords:
        slug, body = body_for_keyword(keyword)
        output_file = OUTPUT_DIR / f"{slug}.md"
        output_file.write_text(body, encoding="utf-8")

    print(f"Done. Generated {len(keywords)} pages in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
