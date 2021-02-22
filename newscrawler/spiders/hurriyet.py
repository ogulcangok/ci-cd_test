
"""
Check url xpath
Check content xpath
parallel?
IP switch and headers
"""
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from newscrawler.items import NewsItem


class HurriyetSpider(CrawlSpider):
    """
    Spider class to get the urls from search results
    """
    name = "hurriyet"
    allowed_domains = ["hurriyet.com.tr"]

    start_urls = ["https://www.hurriyet.com.tr/arama/#/?page=%d&order=Yeniden Eskiye&where=/&how=Article,NewsVideo," \
                  "NewsPhotoGallery,Column,Recipe&startDate=01/01/2000&finishDate=11/02/2021&isDetail=true" % i for i
                  in range(1, 101)]
    rules = (
        Rule(LxmlLinkExtractor(allow=(), restrict_xpaths='/html/body/div[3]/div[1]/div[1]/div/div[1]/div/div['
                                                         '4]/div/div/div/div/div/div/div/div'),
             callback="parse", follow=True),

    )

    def parse(self, response, **kwargs):
        """
        :param response: crawler response of the article url
        :return: parsed doc pushed to elastic
        """
        hxs = Selector(response)
        item = NewsItem()

        item["link"] = response.request.url
        item["lang"] = "tr"
        item["source"] = "hurriyet"
        date_time = hxs.xpath(
            "/html/body/article/div[12]/div/section[1]/header/div[1]/div[2]/div[2]/span[2]/time").extract()
        author = hxs.xpath(
            "/html/body/article/div[12]/div/section[1]/header/section[1]/div[1]/div/div[2]/a[1]/h6").extract()
        title = hxs.xpath("/html/body/article/div[12]/div/section[1]/header/div[2]/div/h1").extract()
        intro = hxs.xpath("/html/body/article/div[12]/div/section[3]/div/h2").extract()
        new_content = hxs.xpath("/html/body/article/div[12]/div/section[3]/div/div[4]").extract()
        new_content = ' '.join(new_content)

        #
        # Processing outputs
        item["intro"] = ' '.join(intro)
        item["title"] = ' '.join(title)
        item["content"] = re.sub(r'\s{2,}', ' ', new_content)

        item["date_time"] = " ".join(date_time)
        item["author"] = " ".join(author)
        return item
