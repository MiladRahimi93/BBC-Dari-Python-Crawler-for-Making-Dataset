import os
import pandas as pd
import json
from datetime import datetime


class Saver:
    def __init__(self, output_dir="data", base_filename="dari_dataset"):
        self.output_dir = output_dir
        self.base_filename = base_filename
        os.makedirs(self.output_dir, exist_ok=True)

    def _timestamped_filename(self, ext="csv"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_dir, f"{self.base_filename}_{timestamp}.{ext}")

    def save_csv(self, articles: list):
        if not articles:
            print("[Saver] No articles to save.")
            return None

        df = pd.DataFrame(articles)
        filepath = self._timestamped_filename("csv")
        df.to_csv(filepath, index=False, encoding="utf-8-sig")
        print(f"[Saver] Saved {len(articles)} articles to {filepath}")
        return filepath

    def save_jsonl(self, articles: list):
        if not articles:
            print("[Saver] No articles to save.")
            return None

        filepath = self._timestamped_filename("jsonl")
        with open(filepath, "w", encoding="utf-8") as f:
            for article in articles:
                f.write(json.dumps(article, ensure_ascii=False) + "\n")

        print(f"[Saver] Saved {len(articles)} articles to {filepath}")
        return filepath
