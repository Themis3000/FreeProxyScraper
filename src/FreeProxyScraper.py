from src.utils import Plugins, GenLimiter, Proxy
from typing import Iterator


class ProxyQuery(Plugins):
    """Handles the querying and operations of plugins"""

    @GenLimiter
    def exec_iter_plugin(self, method_name: str, *args, **kwargs) -> Iterator[Proxy]:
        """Executes a given method in all plugins that return an iterable, then returns an iterable that loops through
        each plugins iterable"""
        for plugin in self.plugins:
            try:
                method = getattr(plugin, method_name)
                return_iter = method(*args, **kwargs)
                for value in return_iter:
                    yield value
            except:
                continue

    def find_proxies(self, limit: int = -1) -> Iterator[Proxy]:
        """Uses all plugins to search for proxies"""
        return self.exec_iter_plugin("find", limit=limit)

    def find_filter(self, limit: int = -1, country: str = None, ping: int = None,
                    min_anon_level: int = 0) -> Iterator[Proxy]:
        """Uses all plugins to finds proxies that meet certain values"""
        return self.exec_iter_plugin("find_filter", country, ping, min_anon_level, limit=limit)
