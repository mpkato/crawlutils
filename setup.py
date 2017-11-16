# -*- coding:utf-8 -*-
from setuptools import setup

setup(
    name = "crawlutils",
    packages = ["crawlutils"],
    version = "0.0.1",
    description = "Crawler Utilities",
    author = "Makoto P. Kato",
    author_email = "kato@dl.kuis.kyoto-u.ac.jp",
    license     = "MIT License",
    url = "https://github.com/mpkato/crawlutils",
    install_requires = [
        "chardet==3.0.4",
        "langid==1.1.6",
        "beautifulsoup4==4.6.0"
    ],
    tests_require=['pytest'],
)
