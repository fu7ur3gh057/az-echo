import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as BS4, ResultSet
from celery.utils.log import get_task_logger

from constants import REQUEST_HEADERS
from utils.link_util import check_negative_site, check_extension

logger = get_task_logger(__name__)


class DrillerService:
    def __init__(self, domain: str, url_pattern: str, page_count: int, negative_tags: list,
                 blacklist: list):
        self.domain = domain
        self.url_pattern = url_pattern
        self.page_count = page_count
        self.negative_tags = negative_tags
        self.blacklist = blacklist

    def start(self, step_number):
        # Increase last step number
        step_number += 1
        result_links = set()
        # Build Search Url
        search_url = self._create_search_page(curr_page_number=step_number)
        logger.info(f'start crawl link {search_url}')
        # Founded links
        links = self._search_links(url=search_url)
        if links is []:
            return {"step_number": step_number, "last_page": search_url, "links": links}
        else:
            for link in links:
                # Trying to make a full URL if starts with /
                if link.startswith('/'):
                    # Getting full link
                    link = self._add_domain_to_url(link)
                    # If URL is not available
                    if not self._page_is_available(link=link):
                        continue
                # Already crawled
                if link in self.blacklist or link in result_links:
                    continue
                else:
                    result_links.add(link)
            result_links = self._extends_domain_url(links=result_links)
            return {"step_number": step_number, "last_page": search_url, "links": result_links}

    def _extends_domain_url(self, links):
        result_links = set()
        for i in links:
            if self.domain in i:
                result_links.add(i)
        return result_links

    def _create_search_page(self, curr_page_number: int):
        return self.url_pattern.replace('$182next_page281$', f'{curr_page_number}')

    def _add_domain_to_url(self, link):
        domain = self.domain
        if domain.endswith('/'):
            domain = domain[:-1]
        return f'{domain}{link}'

    def _page_is_available(self, link: str):
        try:
            request = Request(url=link, headers=REQUEST_HEADERS)
            urlopen(request).read()
            return True
        except Exception as ex:
            print(ex)
            return False

    def _crawl(self, links: ResultSet):
        temp_links = set()
        for tag in links:
            link = tag.get('href', None)
            if link is None or link == '':
                continue
            link = link.replace('\n', '').replace('\r', '')
            link = link.replace('www.', '')
            # checks file extension like .mp4 or .pdf
            if link[0] == '#' or check_extension(url=link):
                continue
            elif link.startswith('//') or link is self.domain or link is self.domain or check_negative_site(link):
                continue
            elif link.__contains__(' ') or link.endswith('.') or link.__contains__('"') or link.__contains__(
                    '"'):
                continue
            elif link.startswith("https://") or link.startswith(
                    'http://') and self.domain in link:  # chance to find URL
                temp_links.add(link)
            elif link[0] == '/' and len(link) > 1:  # chance to find part of base URL
                temp_links.add(link)
            else:
                continue
        return temp_links

    def _search_links(self, url):
        try:
            request = Request(url=url, headers=REQUEST_HEADERS)
            html = urlopen(request).read()
            soup = BS4(html, 'lxml')
            links = soup.find_all('a')
            result = self._crawl(links=links)
            return result
        except Exception as ex:
            print(ex)
            return []
