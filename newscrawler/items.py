# pylint: skip-file
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    """
    Item fields of the article
    """
    link = scrapy.Field()
    lang = scrapy.Field()
    source = scrapy.Field()
    date_time = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    intro = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
