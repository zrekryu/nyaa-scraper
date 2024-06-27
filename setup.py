from setuptools import setup, find_packages

from nyaascraper import __version__

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements.txt", "r", encoding="utf-8") as file:
    requirements = [line.strip() for line in file.read()]

setup(
    name="nyaa-scraper",
    version=__version__,
    description="nyaa-scraper is an asynchronous Python library for scraping nyaa.si and sukebei.nyaa.si, utilizing BeautifulSoup4 and httpx.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ZrekryuDev",
    author_email="zrekryudev@gmail.com",
    url="https://github.com/zrekryu/nyaa-scraper",
    keywords=[
        "nyaa", "sukebei",
        "torrent",
        "asynchronous",
        "web scraping", "beautifulsoup4"
        ],
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries",
        ]
    )