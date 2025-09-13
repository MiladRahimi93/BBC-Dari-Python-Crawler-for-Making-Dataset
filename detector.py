from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

# Ensure consistent results
DetectorFactory.seed = 0


class Detector:
    def __init__(self, target_langs=None, min_chars=50):
        # By default, target Persian (fa) which covers Dari as well
        self.target_langs = target_langs or ["fa"]
        self.min_chars = min_chars

    def is_valid_language(self, text: str) -> bool:
        """
        Check if the text is in Dari/Persian (fa).
        """
        if not text or len(text) < self.min_chars:
            return False

        try:
            lang = detect(text)
            return lang in self.target_langs
        except LangDetectException:
            return False
