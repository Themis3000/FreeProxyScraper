from ..utils.plugins import Proxy, Plugin
from ..utils.soup import get_soup
from typing import Iterator


anon_dict = {"High": 2, "Average": 1, "Low": 1, "no": 0}


class HideMy(Plugin):
    plugin_name = "hidemy.name"
    plugin_url = "https://hidemy.name/en/proxy-list/"

    def find(self) -> Iterator[Proxy]:
        status_code, soup = get_soup("https://hidemy.name/en/proxy-list/")

        if status_code != 200:
            self.report_fail()
            return

        for element in soup.select("div.table_block > table > tbody > tr"):
            entries = element.findChildren(recursive=False)
            yield Proxy(
                ip=entries[0].text,
                port=int(entries[1].text),
                country=entries[2].span.text,
                ping=entries[3].p.text[:-3],
                protocol=entries[4].text.split(",")[0].lower(),
                anon_level=anon_dict[entries[5].text]
            )
