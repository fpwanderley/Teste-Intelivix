# -*- coding: utf-8 -*-

import scrapy

AHNEGAO_URL = 'http://www.ahnegao.com.br/'
AHNEGAO__NEXT_PAGE__XPATH = '//div[@id="wp_page_numbers"]//li[position()=last()]/a/@href'
AHNEGAO__ARTICLE_TITLE_LIST_XPATH = 'article header a'


class AhNegaoSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        AHNEGAO_URL,
    ]

    def parse(self, response):

        for quote in response.css(AHNEGAO__ARTICLE_TITLE_LIST_XPATH):

            yield {
                'article_title': quote.xpath('text()').extract_first(),
            }

        next_page = response.\
            xpath(AHNEGAO__NEXT_PAGE__XPATH).extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)