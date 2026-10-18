"""
Article parser for Brilliant Directories Solution Center HTML pages.
Extracts title, categories, clean text, tables, step lists, and screenshots with context.
"""
import hashlib
from typing import Dict, Any, List
from bs4 import BeautifulSoup

def clean_whitespace(text: str) -> str:
    return " ".join(text.split())

def parse_article_html(html_content: str, url: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html_content, "html.parser")

    # Title extraction
    title = ""
    title_tag = soup.find(["h1", "h2"], class_=lambda c: c and any(k in str(c).lower() for k in ["title", "heading"]))
    if title_tag:
        title = clean_whitespace(title_tag.get_text())
    elif soup.find("h1"):
        title = clean_whitespace(soup.find("h1").get_text())
    elif soup.title:
        title = clean_whitespace(soup.title.get_text().replace("Solution Center", "").replace("Brilliant Directories", "").strip(" :|-"))
    if not title:
        title = url.rstrip("/").split("/")[-1].replace("-", " ").title()

    # Category and Folder extraction from breadcrumbs
    category = "General"
    folder = "Documentation"
    breadcrumbs = soup.find(["nav", "div", "ul"], class_=lambda c: c and "breadcrumb" in str(c).lower())
    if breadcrumbs:
        crumbs = [clean_whitespace(li.get_text()) for li in breadcrumbs.find_all(["li", "a"]) if li.get_text().strip()]
        if len(crumbs) >= 2:
            category = crumbs[1]
        if len(crumbs) >= 3:
            folder = crumbs[2]

    # Article main container
    article_body = soup.find(["article", "div", "section"], class_=lambda c: c and any(k in str(c).lower() for k in ["article-body", "article__body", "solution-content", "content", "post-content"]))
    if not article_body:
        article_body = soup.find("body") or soup

    # Extract tables into markdown representation
    for table in article_body.find_all("table"):
        headers = [clean_whitespace(th.get_text()) for th in table.find_all("th")]
        rows = []
        for tr in table.find_all("tr"):
            cells = [clean_whitespace(td.get_text()) for td in tr.find_all(["td", "th"])]
            if cells:
                rows.append(" | ".join(cells))
        if rows:
            md_table = "\n" + "\n".join(rows) + "\n"
            table.replace_with(soup.new_string(md_table))

    # Extract images with surrounding context
    images_found: List[Dict[str, Any]] = []
    for img in article_body.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if not src:
            continue
        # Ignore small icons, badges, tracking pixels
        if any(ignore in src.lower() for ignore in ["icon", "logo", "avatar", "badge", "tracker", "1x1", ".svg"]):
            continue
        
        alt = clean_whitespace(img.get("alt", ""))
        # Get adjacent text context (parent or sibling text)
        parent_text = ""
        parent = img.parent
        if parent:
            parent_text = clean_whitespace(parent.get_text()[:250])

        images_found.append({
            "image_url": src,
            "alt_text": alt or "Solution center screenshot showing configuration settings",
            "context": parent_text
        })

    # Sections extraction based on H2/H3
    sections: List[Dict[str, str]] = []
    current_heading = "Overview"
    current_content = []

    for elem in article_body.descendants:
        if elem.name in ["h2", "h3", "h4"]:
            if current_content:
                text_block = clean_whitespace(" ".join(current_content))
                if len(text_block) > 20:
                    sections.append({"heading": current_heading, "content": text_block})
                current_content = []
            current_heading = clean_whitespace(elem.get_text())
        elif elem.name in ["p", "li"] and not elem.find(["p", "li"]):
            txt = clean_whitespace(elem.get_text())
            if txt:
                current_content.append(txt)

    if current_content:
        text_block = clean_whitespace(" ".join(current_content))
        if len(text_block) > 20:
            sections.append({"heading": current_heading, "content": text_block})

    # Overall clean text
    full_clean_text = "\n\n".join([f"## {s['heading']}\n{s['content']}" for s in sections])
    if not full_clean_text:
        full_clean_text = clean_whitespace(article_body.get_text())

    # Compute content hash
    content_hash = hashlib.md5(full_clean_text.encode("utf-8")).hexdigest()

    return {
        "url": url,
        "title": title,
        "category": category,
        "folder": folder,
        "sections": sections,
        "clean_text": full_clean_text,
        "images": images_found,
        "content_hash": content_hash
    }
