import inspect
import importlib.util
import glob
import os
import logging
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from dataclasses import dataclass
from abc import abstractmethod, ABC
from typing import List, Iterator, Tuple, Dict
from types import ModuleType

ua = UserAgent()


def get_soup(url: str, random_agent: bool = True, **kwargs) -> Tuple[int, BeautifulSoup]:
    """handles getting a soup from a given url"""
    if random_agent:
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["User-Agent"] = ua.random

    page = requests.get(url, **kwargs)
    return page.status_code, BeautifulSoup(page.content, 'html.parser')


def get_classes(module: ModuleType) -> List[type]:
    """Gets classes in a module"""
    return [_class for name, _class in inspect.getmembers(module, inspect.isclass)]


def class_has_parent(_class: type, parent_class: type) -> bool:
    """Checks if a class has a given parent class"""
    for base in _class.__bases__:
        if base == parent_class:
            return True
    return False


def get_classes_with_parent(module: ModuleType, parent_class: type) -> List[type]:
    """Gets classes in a module with a given parent"""
    return [_class for _class in get_classes(module) if class_has_parent(_class, parent_class)]


class GenLimiter:
    """A decorator used to limit the amount of iterations possible from a generator"""
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self.limit = kwargs.pop("limit", -1)
        self.gen = self.func(*args, **kwargs)
        return self

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            return self.__call__(instance, *args, **kwargs)
        return wrapper

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit == 0:
            raise StopIteration()
        self.limit -= 1
        return next(self.gen)


@dataclass
class Proxy:
    ip: str
    port: int
    protocol: str
    country: str = "unknown"
    ping: int = None
    anon_level: int = 0

    @property
    def address(self) -> str:
        """Gets the full form address for the proxy used for connecting"""
        return f"{self.protocol}://{self.ip}:{self.port}"

    def test(self) -> bool:
        """Tests the proxy to see if it's operational"""
        # todo implement proxy test method
        return True


class Plugin(ABC):
    """Represents a plugin"""
    enabled = True
    fails = 0
    plugin_url: str
    plugin_name: str

    @abstractmethod
    def find(self) -> Iterator[Proxy]:
        """Finds proxies in a plugin"""

    def test(self) -> bool:
        """Tests if the plugin is working"""
        try:
            return not next(self.find(), None) is None
        except:
            return False

    def find_filter(self, country: str = None, ping: int = None, min_anon_level: int = 0) -> Iterator[Proxy]:
        """Finds proxies that meet certain values"""
        for proxy in self.find():
            # Checks if the country is wrong
            if country is not None and not country == proxy.country:
                continue
            # Checks if the ping is too high
            if ping is not None and (proxy.ping is None or not ping >= proxy.ping):
                continue
            # Checks if the anon level is too low
            if not min_anon_level <= proxy.anon_level:
                continue
            # Only yields proxy if all tests where passed
            yield proxy

    @classmethod
    def report_fail(cls):
        """Reports a failed request, must be utilized in child classes"""
        cls.fails += 1


class Plugins:
    """Represents a pool of plugins and handles the loading of them"""
    def __init__(self, import_plugins=True):
        self.plugins = []
        if import_plugins:
            plugin_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plugins")
            self.import_plugin_files(plugin_folder)

    def import_plugin_file(self, path: str, do_test: bool = True) -> None:
        """Imports plugins from a file given a path. do_test first tests if a plugin is working before loading it. If
        the plugin does not pass the test, it is not loaded"""
        # Loads file
        spec = importlib.util.spec_from_file_location("plugins.plugin", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # Get plugins in file
        plugins = get_classes_with_parent(module, Plugin)
        # Test plugins and import them if working
        for plugin_class in plugins:
            plugin = plugin_class()

            if not plugin.enabled:
                continue

            if do_test:
                if not plugin.test():
                    logging.warning(f"Plugin {plugin.plugin_name} at {path} does not seem to be working, and therefore "
                                    f"was not loaded")
                    continue

            self.plugins.append(plugin)

    def import_plugin_files(self, dir_path: str, do_test: bool = True) -> None:
        """Imports all .py files in a directory as plugins"""
        plugin_paths = glob.glob(os.path.join(dir_path, "*.py"))
        for path in plugin_paths:
            self.import_plugin_file(path, do_test)
