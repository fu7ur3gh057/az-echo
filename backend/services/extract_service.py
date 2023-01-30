from bs4 import BeautifulSoup as BS4
from htmldate import find_date
from newspaper import Article
from celery.utils.log import get_task_logger
from utils.lang_util import check_lang
from goose3 import Goose

logger = get_task_logger(__name__)


class ExtractService:
    def __init__(self, url: str, lang: str, negative_words: list):
        self.url = url
        self.lang = lang
        self.negative_words = negative_words

    # Start Extract Text
    def start(self) -> str:
        result_text = ''
        try:
            result_text = self._extract_by_newspaper()
            if result_text == '':
                result_text = self._extract_by_goose()
            text1 = self._extract_by_goose()
            if not check_lang(text=result_text, lang=self.lang):
                result_text = ''
        except Exception as ex:
            print(ex)
            result_text = ''
        finally:
            # result_text = self._replace_negative_words(text=result_text)
            return result_text

    def _replace_negative_words(self, text: str) -> str:
        result_text = text
        text_len = len(result_text)
        for word in self.negative_words:
            word_len = len(word)
            # Replace first words
            if result_text.startswith(word):
                result_text = result_text[word_len: text_len]
            # Replace end words
            if result_text.endswith(word):
                result_text = result_text[0: text_len - word_len]
        return result_text

    # Main method, extracting by newspaper3k
    def _extract_by_newspaper(self) -> str:
        article = Article(self.url, self.lang)
        article.download()
        article.parse()
        return article.text.strip()

    # Alt method, extracting by goose3
    def _extract_by_goose(self) -> str:
        goose = Goose({'use_meta_language': False, 'target_language': self.lang})
        article = goose.extract(url=self.url)
        text = article.cleaned_text
        return article.cleaned_text.strip()
