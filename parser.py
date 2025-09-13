from bs4 import BeautifulSoup
from datetime import datetime


class Parser:
    def __init__(self):
        pass

    def parse_article(self, html, url, category=None):
        """
        Extracts article metadata and content from BBC Persian/Dari article page.
        """
        soup = BeautifulSoup(html, "html.parser")

        # Title
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else None

        # Date
        date_tag = soup.find("time")
        if date_tag and date_tag.has_attr("datetime"):
            try:
                date_published = datetime.fromisoformat(date_tag["datetime"]).isoformat()
            except Exception:
                date_published = date_tag.get_text(strip=True)
        else:
            date_published = None

        # Author
        author_tag = soup.find("span", {"class": "byline__name"})
        author = author_tag.get_text(strip=True) if author_tag else None

        # Content
        paragraphs = soup.find_all("p")
        content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        # Summary (if available)
        summary_tag = soup.find("p", {"class": "bbc-1qew3k6 e1cc2ql70"})
        summary = summary_tag.get_text(strip=True) if summary_tag else None

        return {
            "title": title,
            "date": date_published,
            "author": author,
            "category": category,
            "summary": summary,
            "content": content,
            "url": url,
        }
