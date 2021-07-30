### This project is currently in a non-working state and is unpublished
The framework for this project is built up, however no plugins that implement fetching proxies from actual websites have been created yet. No tests or docs has been created yet either

## FreeProxyScraper
This is a plugin driven web scraper meant to retrieve and test free proxies for use.

## Installation
Run the following to install:

```bash
pip install FreeProxyScraper
```

## Usage

```python
import FreeProxyScraper

proxies = FreeProxyScraper.find(limit=30)
print(proxies)
```

## Development
to install FreeProxyScraper, along with the tools you need to develop, run the following in the directory containing this repo:

```bash
pip install -e .[dev]
```
