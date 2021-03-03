#!/home/ogulcan/translation/venv/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 09:34:44 2021

@author: ogulcan
"""

import re
from datetime import datetime
from time import mktime
import feedparser

feeds = ["https://www.ntv.com.tr/saglik.rss",
         "http://www.haberturk.com/rss/kategori/saglik.xml",
         "https://www.cnnturk.com/feed/rss/saglik/news",
         "https://www.ahaber.com.tr/rss/saglik.xml",
         "https://www.sabah.com.tr/rss/saglik.xml",
         "https://www.sozcu.com.tr/kategori/saglik/rss",
         "https://www.takvim.com.tr/rss/galeri/saglik.xml",
         "http://www.gazetevatan.com/rss/saglik.xml"
         ]


class Article:
    title: str
    link: str
    date: str
    source: str

    def __init__(self, title, link, date):
        self.title = title
        self.link = link
        self.date = date


docs = {}
for feed in feeds:
    d = feedparser.parse(feed)
    source = re.search(r"^((http[s]?|ftp):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.*)?(#[\w\-]+)?$",
                       feed).group(3)
    docs[source] = []
    entries = d["entries"]
    for i in entries:

        try:
            date = dt = datetime.fromtimestamp(mktime(i["published_parsed"]))
        except KeyError:
            date = ""
        article = Article(title=i["title"].replace("<![CDATA[", "").replace("]]>", ""), link=i["link"], date=date)
        docs[source].append(article.__dict__)






