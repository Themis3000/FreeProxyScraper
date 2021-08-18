### This project is currently unpublished
The framework for this project is built up, however there aren't many plugins. The code isn't very stable yet due to the nature of proxy websites rate limiting very quickly. Also, no tests or docs has been created yet. Despite all this, this project *should* be in a working condition.

## FreeProxyScraper
This is a plugin driven web scraper meant to retrieve and test free proxies for use.

## Installation (This doesn't work yet)
Run the following to install:

```bash
pip install FreeProxyScraper
```

## Usage

```python
from FreeProxyScraper import ProxyQuery

pq = ProxyQuery()

for proxy in pq.find(limit=20):
    print(proxy)
```

## Development
to install FreeProxyScraper, along with the tools you need to develop, run the following in the directory containing this repo:

```bash
pip install -e .[dev]
```

If you'd like to contribute to development, right now the most needed thing is writing more plugins. In order to help, you need basic knowledge of BeautifulSoup4. Check out `src/plugins/examplePlugin.py` to see an example layout of a plugin file.