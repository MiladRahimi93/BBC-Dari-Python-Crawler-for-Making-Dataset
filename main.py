# main.py (robust version)
import yaml
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from fetcher import Fetcher
from parser import Parser
from cleaner import Cleaner
from detector import Detector
from saver import Saver

# -------------------------
# Load configuration
# -------------------------
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

sources = config.get("sources", {})
crawler_conf = config.get("crawler", {})
output_conf = config.get("output", {})
lang_conf = config.get("language", {})

# optional limits
MAX_ARTICLES_PER_CATEGORY = crawler_conf.get("max_articles_per_category", 50)

# -------------------------
# Initialize modules
# -------------------------
fetcher = Fetcher(
    user_agents=crawler_conf.get("user_agents"),
    delay=crawler_conf.get("delay_seconds", 2),
    retries=crawler_conf.get("retries", 3),
)
parser = Parser()
cleaner = Cleaner()
detector = Detector(
    target_langs=lang_conf.get("target_langs", ["fa"]),
    min_chars=lang_conf.get("min_chars", 50),
)
saver = Saver(
    output_dir=output_conf.get("directory", "data"),
    base_filename=output_conf.get("base_filename", "dari_dataset"),
)

all_articles = []

def is_bbc_url(url):
    parsed = urlparse(url)
    return parsed.netloc.endswith("bbc.com") or parsed.netloc == ""

def normalize_category_url(base_url, category):
    """
    If category is already a full URL, return it.
    Otherwise join with base_url.
    """
    if not category:
        return None
    category = str(category).strip()
    if category.startswith("http://") or category.startswith("https://"):
        return category
    # allow values like "/persian/topics/..." or "persian/topics/..."
    return urljoin(base_url + "/", category)

def extract_article_links_from_category(html, base_url):
    """
    Extract candidate article URLs from a category/topic page.
    heuristic: include links that contain '/persian/' but exclude '/persian/topics/'
    """
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        full = urljoin(base_url, href)
        parsed = urlparse(full)
        path = parsed.path or ""
        # skip external
        if parsed.netloc and "bbc.com" not in parsed.netloc:
            continue
        # skip topic pages
        if "/persian/topics/" in path:
            continue
        # include likely article pages under /persian/
        if path.startswith("/persian/") and len(path) > len("/persian/"):
            # avoid index/home links that are just '/persian' or '/persian/'
            links.add(full)
    return links

# -------------------------
# Crawl articles
# -------------------------
for source_name, source_info in sources.items():
    base_url = source_info.get("base_url")
    categories = source_info.get("categories", [])
    print(f"[Main] Crawling source: {source_name} ({base_url})")

    for raw_cat in categories:
        try:
            category_url = normalize_category_url(base_url, raw_cat)
            if not category_url:
                continue
            print(f"[Main] Crawling category: {category_url}")

            cat_html = fetcher.get(category_url)
            if not cat_html:
                print(f"[Main] Warning: could not fetch category page: {category_url}")
                continue

            # Extract article links from this category/topic page
            article_links = extract_article_links_from_category(cat_html, base_url)
            if not article_links:
                print(f"[Main] No article links discovered on {category_url} (page may be JS-rendered).")
                continue

            # limit per category to avoid overload
            article_links = sorted(article_links)
            article_links = article_links[:MAX_ARTICLES_PER_CATEGORY]
            print(f"[Main] Found {len(article_links)} candidate article links (limited to {MAX_ARTICLES_PER_CATEGORY}).")

            for i, article_url in enumerate(article_links, start=1):
                print(f"[Main] ({i}/{len(article_links)}) Fetching article: {article_url}")
                art_html = fetcher.get(article_url)
                if not art_html:
                    continue

                article = parser.parse_article(art_html, article_url, category=category_url)
                if not article:
                    continue

                cleaned = cleaner.clean_article(article)
                content = cleaned.get("content", "") or cleaned.get("summary", "") or ""
                if detector.is_valid_language(content):
                    all_articles.append(cleaned)
                    print(f"[Main] Saved article: {cleaned.get('title')}")
                else:
                    print(f"[Main] Skipped (language filter): {article_url}")

        except Exception as exc:
            print(f"[Main] Error while processing category {raw_cat}: {exc}")

# -------------------------
# Save dataset
# -------------------------
if all_articles:
    saver.save_csv(all_articles)
    saver.save_jsonl(all_articles)
else:
    print("[Main] No valid articles found.")
