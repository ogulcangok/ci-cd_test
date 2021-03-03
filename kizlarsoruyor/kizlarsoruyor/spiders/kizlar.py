"""
Ask if answers are needed
exclude author page
"""
import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from kizlarsoruyor.items import NewsItem


class KizlarSpider(CrawlSpider):
    """
    Spider class to get articles from kizlarsoruyor.com
    """
    name = "kizlar"

    allowed_domains = ["kizlarsoruyor.com"]

    def __init__(self, query, *args, **kwargs):
        super(KizlarSpider, self).__init__(*args, **kwargs)

        url = "https://www.kizlarsoruyor.com/ara?q=%s&p=1&t=tumu" % query
        self.start_urls = [url]

    rules = (
        Rule(LxmlLinkExtractor(
            restrict_xpaths="/html/body/section/section/div[1]/div[3]/div/div/div/div/div/div/h3/span/a"),
            callback="parse",
            follow=True),
        Rule(LxmlLinkExtractor(
            restrict_xpaths="//link[@ref='next']"),
            callback="parse_next",
            follow=True
        ),

    )

    def parse_next(self, response):
        """
        :param response: url got from first rule to get the next page
        :return: scrapy response to call the parse
        """
        # TODO: find a way to parse the next urls
        url = response.request.url
        print(url)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        :param response: crawler response of the article url
        :return: parsed doc pushed to elastic
        """
        hxs = Selector(response)
        item = NewsItem()

        item["link"] = response.request.url
        item["lang"] = "tr"
        item["source"] = "kizlarsoruyor"
        item["category"] = " ".join(hxs.xpath("//a[@class='no-posting tgec']/text()").extract())
        date_time = hxs.xpath("//span[@class='posted-on']/text()").extract()

        author = hxs.xpath("//span[@class='name']/text()").extract()
        if author:
            item["author"] = " ".join(author)
        else:
            author = hxs.xpath("//a[@class='username profile-hover']/text()").extract()
            item["author"] = " ".join(author)
        title = hxs.xpath("//h1/text()").extract()

        new_content = hxs.xpath("//div[@class='detail-body']/text()").extract()
        if new_content:
            new_content = ' '.join(new_content)
        else:
            new_content = hxs.xpath("//div[@class='article-body post-body clearfix']/text()")
            new_content = ' '.join(new_content)

        item["title"] = ' '.join(title)
        item["content"] = re.sub(r'\s{2,}', ' ', new_content)

        item["date_time"] = " ".join(date_time)

        return item
