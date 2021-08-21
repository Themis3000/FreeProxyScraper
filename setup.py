from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="FreeProxyScraper",
    version="0.1.1",
    description="A plugin driven package that scrapes sites for free proxies",
    py_modules=["FreeProxyScraper"],
    package_dir={"": "src"},
    packages=["utils", "plugins"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
        "beautifulsoup4",
        "fake-useragent"
    ],
    extras_require={
        "dev": [
            "pytest"
        ]
    },
    url="https://github.com/themis3000/fillinthis",
    author="Themi Megas",
    author_email="tcm4760@gmail.com"
)

