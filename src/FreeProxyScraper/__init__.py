import logging
from .utils.plugins import Plugins, Proxy
from .utils.decos import GenLimiter
from typing import Iterator


class ProxyQuery(Plugins):
    """Handles the querying and operations of plugins"""

    @GenLimiter
    def exec_iter_plugin(self, method_name: str, sort_asc_fails: bool = True, *args, **kwargs) -> Iterator[Proxy]:
        """Executes a given method in all plugins that return an iterable, then returns an iterable that loops through
        each plugins iterable"""
        if sort_asc_fails:
            self.plugins.sort(key=lambda plugin: plugin.fails)

        for plugin in self.plugins:
            try:
                method = getattr(plugin, method_name)
                return_iter = method(*args, **kwargs)
                for value in return_iter:
                    yield value
            except Exception:
                logging.info(f"FreeProxyScraper plugin \"{plugin.plugin_name}\" has crashed")
                plugin.report_fail()
                continue

    @GenLimiter
    def find_proxies(self, test: bool = True) -> Iterator[Proxy]:
        """Uses all plugins to search for proxies"""
        proxies = self.exec_iter_plugin("find", True)

        if test:
            proxies = self.test_proxies(proxies)

        return proxies


    @GenLimiter
    def find_filter(self, country: str = None, ping: int = None,
                    min_anon_level: int = 0, test: bool = True) -> Iterator[Proxy]:
        """Uses all plugins to finds proxies that meet certain values"""
        proxies = self.exec_iter_plugin("find_filter", True, country, ping, min_anon_level)

        if test:
            proxies = self.test_proxies(proxies)

        return proxies


    def test_proxies(self, proxies: Iterator[Proxy]) -> Iterator[Proxy]:
        """Takes a iterator of Proxy and returns a generator that skips over every plugin that failed the test"""
        for proxy in proxies:
            if proxy.test():
                yield proxy
