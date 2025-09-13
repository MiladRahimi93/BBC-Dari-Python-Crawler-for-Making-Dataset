"""
collect_topics.py

Run this locally in your crawler project directory.

What it does:
- Fetches https://www.bbc.com/persian
- Extracts all links matching /persian/topics/<...>
- Optionally follows article links found on the homepage (depth=1) to discover more topic pages
- Saves unique topic URLs to topics_list.txt
- Optionally updates config.yaml (replaces categories with the found URLs)

Usage:
    python collect_topics.py

Requirements:
    pip install requests beautifulsoup4 pyyaml
"""

import re
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import yaml

BASE = "https://www.bbc.com/persian"
OUTPUT_FILE = "topics_list.txt"
CONFIG_FILE = "config.yaml"
USER_AGENT = "Mozilla/5.0 (compatible; BBCTopicCollector/1.0; +https://github.com/)"

HEADERS = {"User-Agent": USER_AGENT}
# link pattern for BBC topics pages
TOPIC_RE = re.compile(r"^/persian/topics/[a-z0-9_]+", re.IGNORECASE)
# sometimes topic links may be full absolute URLs, handle both

def fetch(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"[fetch] failed {url}: {e}")
        return None
    time.sleep(1.0)  # polite delay; increase if you like
    return resp.text

def extract_links(html, base_url=BASE):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("http"):
            full = href
        else:
            full = urljoin(base_url, href)
        links.add(full)
    return links

def collect_topics_from_url(url):
    html = fetch(url)
    if not html:
        return set()
    links = extract_links(html, base_url=url)
    topic_urls = set()
    for link in links:
        parsed = urlparse(link)
        path = parsed.path
        if TOPIC_RE.match(path):
            # normalize to absolute BBC URL
            topic_urls.add(urljoin(BASE, path))
    return topic_urls, links

def main():
    print("[main] fetching base:", BASE)
    base_html = fetch(BASE)
    if not base_html:
        print("[main] could not fetch base page. Aborting.")
        return

    all_topic_urls = set()
    # first pass: extract from homepage
    topics, homepage_links = collect_topics_from_url(BASE)
    print(f"[main] found {len(topics)} topic links on homepage")
    all_topic_urls.update(topics)

    # optional: follow article/category links to depth=1 to discover more topics
    # filter homepage links to internal /persian/ paths to limit scope
    internal_links = [l for l in homepage_links if urlparse(l).netloc.endswith("bbc.com") and "/persian/" in urlparse(l).path]
    print(f"[main] following {len(internal_links)} internal links to discover more topics (depth=1). This may take a while.")
    # limit to first N internal links to be polite
    MAX_FOLLOW = 50
    for i, link in enumerate(internal_links[:MAX_FOLLOW], start=1):
        print(f"[main] ({i}/{min(MAX_FOLLOW,len(internal_links))}) checking {link}")
        topics2, _ = collect_topics_from_url(link)
        if topics2:
            all_topic_urls.update(topics2)

    # Save results
    sorted_list = sorted(all_topic_urls)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for u in sorted_list:
            f.write(u + "\n")
    print(f"[main] saved {len(sorted_list)} topic URLs to {OUTPUT_FILE}")

    # Optionally update config.yaml: replace sources.bbc.categories with the list
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as cf:
            cfg = yaml.safe_load(cf)
        if "sources" in cfg and "bbc" in cfg["sources"]:
            # replace categories
            cfg["sources"]["bbc"]["categories"] = sorted_list
            with open(CONFIG_FILE, "w", encoding="utf-8") as cf:
                yaml.dump(cfg, cf, allow_unicode=True, sort_keys=False)
            print(f"[main] Updated {CONFIG_FILE} with {len(sorted_list)} categories.")
        else:
            print(f"[main] {CONFIG_FILE} does not contain expected sources.bbc structure. Skipping update.")
    except FileNotFoundError:
        print(f"[main] {CONFIG_FILE} not found — skipping automatic config update.")
    except Exception as e:
        print(f"[main] warning: failed to update {CONFIG_FILE}: {e}")

if __name__ == "__main__":
    main()
