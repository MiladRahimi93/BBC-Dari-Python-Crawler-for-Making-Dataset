import re


class Cleaner:
    def __init__(self):
        # Mapping Arabic characters to Persian/Dari equivalents
        self.char_map = {
            "ي": "ی",  # Arabic Yeh → Farsi/Dari Yeh
            "ك": "ک",  # Arabic Kaf → Farsi/Dari Kaf
        }

    def normalize_text(self, text: str) -> str:
        """
        Normalize Dari/Persian text.
        """
        if not text:
            return ""

        # Replace Arabic characters with Persian/Dari equivalents
        for arabic, dari in self.char_map.items():
            text = text.replace(arabic, dari)

        # Remove multiple spaces and newlines
        text = re.sub(r"\s+", " ", text).strip()

        # Remove weird invisible characters
        text = re.sub(r"[\u200c\u200d]", "", text)  # zero-width chars

        return text

    def clean_article(self, article: dict) -> dict:
        """
        Cleans all text fields in an article dictionary.
        """
        for field in ["title", "author", "summary", "content"]:
            if field in article and article[field]:
                article[field] = self.normalize_text(article[field])
        return article
