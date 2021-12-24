# FreeProxyScraper
This is a plugin driven web scraper meant to retrieve and test free proxies for use. Note that this package may be unstable and should not be used in a production environment.

## Installation
Run the following to install:

```bash
pip install FreeProxyScraper
```

## Usage

```python
import FreeProxyScraper

pq = FreeProxyScraper.ProxyQuery()

# Returns any proxy's found
for proxy in pq.find_proxies(limit=20):
    print(proxy)

# Returns only proxies that are anonymous or "elite"
for proxy in pq.find_filter(limit=20, min_anon_level=1):
    print(proxy)
```

There are 3 anonymity levels, indicated as integers between 0-2.

- Level 0: Transparent. The end server can see your real ip even though it's being routed through a proxy
- Level 1: Anonymous. The end server knows you are using a proxy, but does not know your real ip
- Level 2: High Anonymity, also sometimes called "elite". The end server does not know you are using a proxy or know your real ip. The end server may have a database known proxies, so they still may know that you are using a proxy by matching your ip against such a database.

## List of sites implemented for scraping:
- https://www.sslproxies.org/
- http://free-proxy.cz/en/
- https://spys.one/en/
- https://hidemy.name/en/proxy-list/
- https://geonode.com/free-proxy-list

## FAQ

- Help! It isn't working!

Proxies are checked to see if they are truely transparent or not automatically by making a request to a remote http server, which returns information on what the recived request looked like. This package uses http://themiserver.duckdns.org:5001/ in order to achive that. The http server is ran from my home, so it may have outages here and there if I ever need to restart my server. If you need to know that this package will behave in a stable way, use test=False when invoking the find_filter method. e.g. `find_filter(limit=20, min_anon_level=1, test=False)`

- Why implement so many websites for scraping?

Websites are always changing, or going down, or banning ip's very quickly. In order to make sure this package stays reliable it is essential that it implements many websites

- I want to make sure that I am truly not using transparent proxies, how do I know the websites being scraped from aren't lying abut the anonymity of the proxies?

By default, all proxies will be checked if they are transparent or not before ever giving them to you if you specified a higher anon_level then 0. There's no need to worry, your ip should be safe.

## Development
to install FreeProxyScraper, along with the tools you need to develop, run the following in the directory containing this repo:

```bash
pip install -e .[dev]
```

If you'd like to contribute to development, right now the most needed thing is writing more plugins. In order to help, you need basic knowledge of BeautifulSoup4 and a little of patience with websites purposely making it hard for you to scrape information. Check out `src/plugins/examplePlugin.py` to see an example layout of a plugin file.
