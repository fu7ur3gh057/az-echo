import datetime
import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as BS4
from celery.utils.log import get_task_logger

from constants import REQUEST_HEADERS
from utils.link_util import check_extension, check_wrong_symbols, get_clean_url, \
    has_negative_tag, check_negative_site, compare_urls_date

logger = get_task_logger(__name__)


class DiscoverService:
    def __init__(self, domain: str, search_url: str, negative_tags: list, blacklist: list | None = None, lang='az'):
        self.domain = domain
        self.search_url = search_url
        self.lang = lang
        self.negative_tags = negative_tags
        self.blacklist = blacklist
        self.today = datetime.date.today()

    # Main method, researching new links
    def start(self) -> dict | None:
        try:
            request = Request(url=self.search_url, headers=REQUEST_HEADERS)
            html = urlopen(request).read()
            soup = BS4(html, 'lxml')
            links = soup.find_all('a')
            temp_links = self._filter(links, black_list=self.blacklist)
            new_links = self._verify_upload_date(links=temp_links)
            return {'blacklist': temp_links, 'new_links': new_links}
        except Exception as ex:
            print(ex)
            return None

    # Adding domain to cutted url
    # EX: /ru/criminal/3123 -> https://report.az/ru/criminal/3123
    # link should starts with slash: /ru/page=352
    def _add_domain_to_url(self, link):
        domain = self.domain
        if domain.endswith('/'):
            domain = domain[:-1]
        return f'{domain}{link}'

    # Finding potential links. links should start with /
    def _find_potential_links(self, link, links):
        full_link = self._add_domain_to_url(link)
        if full_link in links:
            return False
        try:
            request = Request(url=full_link, headers=REQUEST_HEADERS)
            urlopen(request).read()
            return True
        except Exception as ex:
            print(ex)
            return False

    # Filter all founded links
    def _filter(self, links, black_list):
        clean_domain = get_clean_url(url=self.domain)
        # Potential links that starts with slash /
        potential_links = set()
        # Temporary Links
        temp_links = set()
        for tag in links:
            link = tag.get('href', None)
            if link is not None and link != '':
                if link in black_list:
                    continue
                link = link.replace('\n', '').replace('\r', '')
                link = link.replace('www.', '')
                # Syntactic fail
                if link[0] == '#' or check_extension(url=link) or has_negative_tag(link, self.negative_tags):
                    continue
                # Wrong start of word
                elif link.startswith('//'):
                    continue
                # Wrong symbols
                elif check_wrong_symbols(link=link) or link.endswith('.'):
                    continue
                # Add link to temp_links
                elif link.startswith("https://") or link.startswith('http://'):
                    temp_links.add(link)
                elif link[0] == '/' and len(link) > 1:  # > 1 chance to find part of base URL
                    potential_links.add(link)
                else:
                    continue
        for link in potential_links:
            if self._find_potential_links(link, black_list):
                temp_links.add(self._add_domain_to_url(link))
        return temp_links

    # Verifying current date and upload date
    # difference should not be more than 1 month
    def _verify_upload_date(self, links):
        result = set()
        for link in links:
            time.sleep(0.5)
            if check_negative_site(url=link):
                continue
            else:
                if self.domain in link:
                    if compare_urls_date(url=link, today=self.today):
                        result.add(link)
        return result
