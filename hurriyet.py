from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from ..items import NewsItem
from datetime import datetime
import pandas as pd
import re


class HurriyetSpider(CrawlSpider):
    name = "hurriyet"
    allowed_domains = ["hurriyet.com.tr"]

    def __init__(self, yearmonth='', *args, **kwargs):
        super(HurriyetSpider, self).__init__(*args, **kwargs)
        begin_date = pd.Timestamp(yearmonth + "-01")
        end_date = pd.Timestamp(begin_date) + pd.DateOffset(months=1) - pd.DateOffset(days=1)
        date_inds  = [d.date().isoformat().replace("-","") for d in pd.date_range(begin_date,end_date)]
        self.start_urls = ["http://www.hurriyet.com.tr/index/?d=%s" % d for d in date_inds]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="news"]/div[@class="desc"]//a',)), callback="parse_items", follow= True),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="paging"]/a',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        item = NewsItem()
        item["link"] = response.request.url
        item["lang"] = "tr"
        item["source"] = "hurriyet"
        category     = hxs.xpath("//div[@class='col-md-12']/div[@class='breadcrumb-body clr']/span//text()").extract()
        date_time    = hxs.xpath("//span[@class='modify-date']/text()").extract()
        item["author"]   = ""
        title            = hxs.xpath("//h1[@class='news-detail-title selectionShareable']/text()").extract()
        intro            = hxs.xpath("//div[@class='news-detail-spot news-detail-spot-margin']/h2/text()").extract()
        new_content      = hxs.xpath("//div[@class='news-box']/p/text()").extract()
        #
        # Processing outputs
        item["intro"]      = ' '.join(intro)
        item["title"]      = ' '.join(title)
        new_content        = ' '.join(new_content)
        new_content        = re.sub('\n',' ',new_content)
        item["content"]    = re.sub('\s{2,}',' ',new_content)
        category           = category[1:-1]
        category           = [c for c in category if not c==">"]
        item["category"]   = '|'.join(category)
        item["date_time"]  = " ".join(date_time)
        '''date_time = re.split("\s:\s|\s-\s",date_time[0])
        date      = date_time[1]
        time      = date_time[2].split(":")
        date      = date.split()
        date_time = datetime(int(date[2]),
                            int(get_month_from_turkish(date[1])),
                            int(date[0]),int(time[0]),int(time[1]))
        item["date_time"]   = date_time.isoformat() '''
        # items = []
        # for title in titles:
        #     item = CraigslistSampleItem()
        #     item["title"] = title.select("div[@class='desc']//a//text()").extract()
        #     item["link"] = title.select("div[@class='desc']//a/@href").extract()
        #     items.append(item)
        return(item)
