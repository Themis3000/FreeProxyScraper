from src.utils import Proxy, Plugin
from typing import Iterator
from bs4 import BeautifulSoup
import requests
import base64


anon_dict = {"High anonymity": 2, "Anonymous": 1, "Transparent": 0}
request_headers = {
    "Accept": "http://free-proxy.cz/en/",
    "Host": "free-proxy.cz",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
}


class FreeProxy(Plugin):
    plugin_name = "free-proxy"
    plugin_url = "http://free-proxy.cz/en/"

    def find(self) -> Iterator[Proxy]:
        response = requests.get("http://free-proxy.cz/en/", headers=request_headers)
        soup = BeautifulSoup(response.content)

        table_elements = soup.select("table#proxy_list > tbody > tr")
        for element in table_elements:
            entries = element.findChildren(recursive=False)

            # Ip's are encoded in base 64 and wrapped in js code meant for the browser to decode it.
            ip_code = entries[0].script.string
            # Sometimes an element is just a google ad, in that case ip_code will be none
            if ip_code is None:
                continue
            ip_encoded = ip_code[30:-3]  # Trims out js code, leaving just the base64
            ip = base64.b64decode(ip_encoded).decode("utf-8")  # Decodes the base64

            port = int(entries[1].string)
            protocol = entries[2].string.lower()
            country = entries[3].a.string

            anon_str = entries[6].string
            anon_level = anon_dict[anon_str]

            ping = int(entries[9].div.small.string[:-3])

            yield Proxy(ip=ip, port=port, protocol=protocol, country=country, anon_level=anon_level, ping=ping)
