"""
@author: Ogulcan
"""

from scrapy.exceptions import CloseSpider
from scrapy.spiders import Spider, Request
from ..items import NewsItem


class EksiScraper(Spider):
    """
    Spider class to get articles from eksisozluk.com
    """
    name = "eksisozluk"

    allowed_domains = ["eksisozluk.com"]

    def __init__(self, query, *args, **kwargs):
        super(EksiScraper).__init__(*args, **kwargs)

        url = "https://eksisozluk.com/%s" % query
        self.start_urls = [url]

    def parse(self, response, **kwargs):
        """
        :param response:
        :param kwargs:
        :return:
        """
        items_to_scrape = response.xpath('//*[@id="topic"]/ul/li')
        if len(items_to_scrape) == 0:
            raise CloseSpider('no_item_found')


        for sel in items_to_scrape:

            title = response.xpath('//*[@id="title"]/a/span/text()').extract()[0]
            date = sel.xpath('//a[@class="entry-date permalink"]/text()').extract()[0]
            text = sel.xpath('//div[@class="content"]/text()').extract()[0].strip()
            author = sel.xpath('//a[@class="entry-author"]/text()').extract()[0]

            item = NewsItem()
            item['source'] = self.name
            item['title'] = title
            item['date_time'] = date
            item['content'] = text
            item['author'] = author
            item["lang"] = "tr"

            yield item

        current_page = int(response.xpath('//*[@class="pager"]/@data-currentpage').extract()[0])
        page_count = int(response.xpath('//*[@class="pager"]/@data-pagecount').extract()[0])

        current_url = response.request.url.split('?p')[0]

        next_page = current_page + 1
        if page_count >= next_page:
            # if current_page < 1:
            yield Request('%s?p=%s' % (current_url, next_page))
