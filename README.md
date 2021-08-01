### This project is currently in a non-working state and is unpublished
The framework for this project is built up, however there aren't many plugins. Code isn't very stable yet due to the nature of proxy websites rate limiting very quickly. Also, no tests or docs has been created yet

## FreeProxyScraper
This is a plugin driven web scraper meant to retrieve and test free proxies for use.

## Installation
Run the following to install:

```bash
pip install FreeProxyScraper
```

## Usage

```python
from FreeProxyScraper import ProxyQuery

pq = ProxyQuery()

for proxy in pq.find(limit=30):
    print(proxy)
```

## Development
to install FreeProxyScraper, along with the tools you need to develop, run the following in the directory containing this repo:

```bash
pip install -e .[dev]
```
