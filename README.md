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

for proxy in pq.find_proxies(limit=20):
    print(proxy)
```

## List of sites implemented for scraping:
- https://www.sslproxies.org/
- http://free-proxy.cz/en/
- https://spys.one/en/
- https://hidemy.name/en/proxy-list/
- https://geonode.com/free-proxy-list

## FAQ
- Why implement so many websites for scraping?

Websites are always changing, or going down, or banning ip's very quickly. In order to make sure this package stays reliable it is essential that it implements many websites

## Development
to install FreeProxyScraper, along with the tools you need to develop, run the following in the directory containing this repo:

```bash
pip install -e .[dev]
```

If you'd like to contribute to development, right now the most needed thing is writing more plugins. In order to help, you need basic knowledge of BeautifulSoup4 and a little of patience with websites purposely making it hard for you to scrape information. Check out `src/plugins/examplePlugin.py` to see an example layout of a plugin file.