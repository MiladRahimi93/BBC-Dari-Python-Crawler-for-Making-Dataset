import time
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Fetcher:
    def __init__(self, user_agents=None, delay=2, retries=3, backoff=0.3):
        self.user_agents = user_agents or [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ]
        self.delay = delay

        self.session = requests.Session()
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, url):
        headers = {"User-Agent": random.choice(self.user_agents)}
        try:
            response = self.session.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            time.sleep(self.delay)  # polite crawling
            return response.text
        except requests.RequestException as e:
            print(f"[Fetcher] Error fetching {url}: {e}")
            return None
