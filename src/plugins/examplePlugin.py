from utils.plugins import Proxy, Plugin
from utils.soup import get_soup
from typing import Iterator

example_proxy_data = [{"ip": "18.345.23.653", "port": 543, "country": "United States", "anon_level": 1, "protocol": "https", "ping": 43},
                      {"ip": "98.345.675.235", "port": 118, "country": "India", "anon_level": 0, "protocol": "socks", "ping": 98},
                      {"ip": "45.123.543.234", "port": 42, "country": "United States", "anon_level": 2, "protocol": "http", "ping": 10043}]


# The title of the class can be whatever you'd like, but be sure to keep it related
class ExamplePlugin(Plugin):
    enabled = False  # Do not include this line in your version
    # You must include a plugin name and the url you are scraping from
    plugin_name = "example plugin"
    plugin_url = "https://www.example.com/"

    # You must implement the find method. This method should yield each proxy it finds
    def find(self) -> Iterator[Proxy]:
        # Using get_soup() is advised as it will handle making the request and turning it into a soup for you. It will
        # also handle setting a random browser agent for you (although this can be disabled with random_agent = False).
        # Any extra named arguments passed in will be passed directly to a requests.get() call.
        status, soup = get_soup("https://www.example.com/", headers={"example header": "example value"})

        # Be sure to report any failed requests and immediately return so that the package will stop making requests
        # to this site for a while. We don't want to keep making request to site's that have rate limited us.
        if status != 200:
            self.report_fail()
            return

        # Somehow implement looping through scraped proxys and yield each one as a proxy object. Only ip, port, and
        # protocol are required, but obtaining as much information as possible is always best, especially the anon_level
        for proxy_dict in example_proxy_data:
            yield Proxy(
                ip=proxy_dict["ip"],  # string

                port=proxy_dict["port"],  # integer

                # Should be one of the following: https, http, socks4, socks5
                protocol=proxy_dict["protocol"],  # string

                # Should be the country name in camel case, do not report the country code.
                country=proxy_dict["country"],  # string

                # There are 3 anon levels, indicated as integers 0-2.
                # Level 0: Transparent
                # Level 1: Anonymous
                # Level 2: High Anonymity. Also sometimes called "elite"
                anon_level=proxy_dict["anon_level"],  # integer

                # This is supposed to be the ping value as indicated by the website. Do not try to measure ping from the
                # local machine to the proxy directly
                ping=proxy_dict["ping"]  # integer
            )
