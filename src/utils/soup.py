import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from typing import Tuple, Union

ua = UserAgent()


def get_soup(url: str, random_agent: bool = True, **kwargs) -> Tuple[int, Union[None, BeautifulSoup]]:
    """handles getting a soup from a given url"""
    if random_agent:
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["User-Agent"] = ua.random

    try:
        page = requests.get(url, **kwargs)
        soup = BeautifulSoup(page.content, 'html.parser')
    except requests.RequestException:
        return 418, None
    except Exception:
        return page.status_code, None
    return page.status_code, soup