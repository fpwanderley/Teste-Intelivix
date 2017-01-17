# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from AhNegao.items import AhNegaoArticleItem


AHNEGAO__NEXT_PAGE__XPATH = '//div[@id="wp_page_numbers"]//li[position()=last()]/a/@href'


class AhNegaoSpider(BaseSpider):
    name = "ahnegao"
    start_urls = ['http://www.ahnegao.com.br/']

    article_title_xpath = '//article/header//a'
    article_fields = {
        'title': './/text()',
        'page': '//div[@id="wp_page_numbers"]//li[@class="active_page"]/a/text()'
    }

    def parse(self, response):

        selector = Selector(response)

        # Iterate over all articles present in the response.
        for article in selector.xpath(self.article_title_xpath):

            loader = ItemLoader(item=AhNegaoArticleItem(), selector=article)

            # Define the processors
            loader.default_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            # Iterate oer all fields in 'article_field' and scrapes each piece of data.
            for field, xpath in self.article_fields.iteritems():
                loader.add_xpath(field, xpath)

            yield loader.load_item()

        next_page = response.\
            xpath(AHNEGAO__NEXT_PAGE__XPATH).extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse)
