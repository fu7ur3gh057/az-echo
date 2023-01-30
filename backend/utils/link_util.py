import os
import sys

import tldextract as tldextract
from htmldate import find_date

from constants import NEGATIVE_EXTENSIONS, NEGATIVE_SITES

subdomain_exists = lambda url: True if tldextract.extract(url) != '' else False

# https://vk.com/ -> https://vk.com
remove_last_slash = lambda link: link[:-1] if link.endswith('/') else link


# https://ru.vk.com/ -> ru
def get_subdomain(url: str) -> str: return f'{tldextract.extract(url).subdomain}'.lower()


# https://vk.com/ -> vk
def get_clean_domain(url: str) -> str: return f'{tldextract.extract(url).domain}'.lower()


# Block
def block_print():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enable_print():
    sys.stdout = sys.__stdout__


# https://vk.com/ -> vk.com
def get_clean_url(url: str) -> str:
    extracted = tldextract.extract(url)
    return f'{extracted.domain}.{extracted.suffix}'.lower()


# check extensions of url or file name -> .MP4 .PDF
def check_extension(url: str) -> bool:
    result = False
    for extension in NEGATIVE_EXTENSIONS:
        if url.endswith(extension):
            result = True
            break
    return result


def check_negative_site(url) -> bool:
    result = False
    for domain in NEGATIVE_SITES:
        if domain in url:
            result = True
            break
    return result


def check_wrong_symbols(link):
    if ' ' in link or '"' in link or "'" in link:
        return True
    return False


def compare_urls_date(url, today) -> bool:
    result = False
    try:
        # block_print()
        date = find_date(url)
        # enable_print()
        splitted = date.split('-')
        year = int(splitted[0])
        month = int(splitted[1])
        day = int(splitted[2])
        if year == today.year:
            if month == today.month or month == today.month - 1:
                result = True
        return result
    except Exception as ex:
        print(ex)
        return result


def has_negative_tag(link: str, blacklist: list) -> bool:
    trigger = False
    for i in blacklist:
        if i in link:
            trigger = True
    return trigger


def make_full_url(link: str, domain: str) -> str:
    pass
