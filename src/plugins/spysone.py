from src.utils import Proxy, Plugin
from typing import List


class Spysone(Plugin):
    plugin_name = "Spysone"
    plugin_url = "https://spys.one/"

    def find(self) -> List[Proxy]:
        yield Proxy("1.1.1.1", 5959, "https", "US", ping=38, anon_level=3)
        yield Proxy("1.1.2.2", 5958, "socks5", "SW")
        yield Proxy("8.8.8.8", 5959, "http", "US", anon_level=2)
        yield Proxy("2.1.2.2", 5958, "socks4", "UK")
