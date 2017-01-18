# -*- coding: utf-8 -*-

import logging

from scrapy import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose

from AhNegao.items import AhNegaoArticleItem
from util.utils import Log


# For logging
logr = logging.getLogger('ahnegao')

AHNEGAO__NEXT_PAGE__XPATH = '//div[@id="wp_page_numbers"]//li[position()=last()]/a/@href'


class AhNegaoSpider(Spider):
    name = "ahnegao"
    # start_urls = ['http://www.ahnegao.com.br/']
    start_urls = ['http://www.ahnegao.com.br']

    custom_settings = {
        'ITEM_PIPELINES': {
            'AhNegao.pipelines.AhNegaoArticlePipeline': 300,
        }
    }

    article_title_xpath = '//article/header//a'
    article_fields = {
        'title': './/text()',
        'page': '//div[@id="wp_page_numbers"]//li[@class="active_page"]/a/text()'
    }

    def __init__(self, *args, **kwargs):
        Log.add_header(logr, __name__, None, AhNegaoSpider)
        logr.debug("Starting AhNegaoSpider.")

        super(AhNegaoSpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        logr.debug("Parsing AhNegaoSpider Request.")

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

            item = loader.load_item()

            Log.item_yield(logr, item)
            yield item

        next_page = response.\
            xpath(AHNEGAO__NEXT_PAGE__XPATH).extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)

            logr.debug("Requesting next page: {page}: ".format(page=next_page))
            yield Request(next_page, callback=self.parse)

        Log.add_footer(logr)