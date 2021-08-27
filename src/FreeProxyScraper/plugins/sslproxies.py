from ..utils.plugins import Proxy, Plugin
from ..utils.soup import get_soup
from typing import Iterator

anon_dict = {"elite proxy": 2, "anonymous": 1, "transparent": 0}


class SslProxies(Plugin):
    plugin_name = "sslproxies"
    plugin_url = "https://www.sslproxies.org/"

    def find(self) -> Iterator[Proxy]:
        response_code, soup = get_soup("https://www.sslproxies.org/")

        if response_code != 200:
            self.report_fail()
            return

        elements = soup.select("table > tbody > tr")
        for element in elements:
            entries = element.findChildren(recursive=False)
            yield Proxy(
                ip=entries[0].string,
                port=int(entries[1].string),
                country=entries[3].string,
                anon_level=anon_dict[entries[4].string],
                protocol="https"
            )
