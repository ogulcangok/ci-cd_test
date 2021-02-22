
"""
Ask if answers are needed
exclude author page
"""
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from newscrawler.items import NewsItem


class KizlarSpider(CrawlSpider):
    """
    Spider class to get articles from kizlarsoruyor.com
    """
    name = "kizlar"
    allowed_domains = ["kizlarsoruyor.com"]

    start_urls = ["https://www.kizlarsoruyor.com/saglik?p=%d" % i for i in range(1, 101)]

    rules = (
        Rule(LxmlLinkExtractor(allow=(),
                               deny=(["https://www.kizlarsoruyor.com/saglik?t=benceler",
                                      "https://www.kizlarsoruyor.com/saglik?t=sorular",
                                      "https://www.kizlarsoruyor.com/saglik?t=anketler",
                                      "https://www.kizlarsoruyor.com/yemek-tarifler/,"
                                      "https://www.kizlarsoruyor.com/uye/",
                                      "https://www.kizlarsoruyor.com/fenomen/"]),
                               deny_domains=["uye", "fenomen", "yemek-tarifler"],

                               restrict_xpaths=["/html/body/section/section/div[1]/div[3]/div[2]/div"
                                   , "/html/body/section/section/div[1]/div[3]/div[3]/div"
                                   , "/html/body/section/section/div[1]/div[3]/div[4]/div"
                                   , "/html/body/section/section/div[1]/div[3]/div[5]/div"],
                               ),
             callback="parse",
             follow=True),

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
        item["source"] = "kizlarsoruyor"
        date_time = hxs.xpath("//span[@class='posted-on']/text()").extract()

        author = hxs.xpath("//a[@class='name profile-hover']/text()").extract()
        title = hxs.xpath("//h1/text()").extract()
        intro = hxs.xpath("//h2/text()").extract()
        new_content = hxs.xpath("//div[@class='detail-body']/text()").extract()
        if new_content:
            new_content = ' '.join(new_content)
        else:
            new_content = hxs.xpath("//div[@class='article-body post-body clearfix']/text()")
            new_content = ' '.join(new_content)
        item["intro"] = ' '.join(intro)
        item["title"] = ' '.join(title)
        item["content"] = re.sub(r'\s{2,}', ' ', new_content)

        item["date_time"] = " ".join(date_time)
        item["author"] = " ".join(author)
        return item
