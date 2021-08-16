from src.utils import Proxy, Plugin
from typing import Iterator
from bs4 import BeautifulSoup
import requests

anon_dict = {"elite proxy": 2, "anonymous": 1, "transparent": 0}


class SslProxies(Plugin):
    plugin_name = "sslproxies"
    plugin_url = "https://www.sslproxies.org/"

    def find(self) -> Iterator[Proxy]:
        with open("D:\pycharm\FreeProxyScraper\src\plugins\ssl.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        elements = soup.select("table#proxylisttable > tbody > tr")
        for element in elements:
            entries = element.findChildren(recursive=False)
            yield Proxy(
                ip=entries[0].string,
                port=int(entries[1].string),
                country=entries[3].string,
                anon_level=anon_dict[entries[4].string],
                protocol="https"
            )
