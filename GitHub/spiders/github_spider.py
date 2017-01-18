# -*- coding: utf-8 -*-

import logging

from scrapy.spiders import Spider
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join

from GitHub.items import GitHubRepositoryItem
from util.utils import Log

# For logging
logr = logging.getLogger('github')


class GitHubSpider(Spider):
    name = 'github'
    start_urls = ['https://github.com/login']

    custom_settings = {
        'ITEM_PIPELINES': {
            'GitHub.pipelines.GitHubRepositoryPipeline': 200,
        }
    }

    login_form_xpath = './/div[@id="login"]/form'
    login_error_div_xpath = '//div[contains(@class, "flash-error")]'

    user_repos_xpath = '//ul[@id="repo_listing"]/li[@class="{type}"]'
    repo_fields = {
        'repo_name': './/span[@class="repo"]/text()',
    }

    def __init__(self, login='', password='', *args, **kwargs):
        Log.add_header(logr, __name__, None, GitHubSpider)
        logr.debug("Starting GitHubSpider.")

        super(GitHubSpider, self).__init__(*args, **kwargs)

        self.login_form_data = {
            'login': login,
            'password': password
        }

    def parse(self, response):

        logr.debug("Parsing GitHub initial page Request.")

        yield FormRequest.from_response(response,
                                        method='POST',
                                        formxpath=self.login_form_xpath,
                                        formdata=self.login_form_data,
                                        callback=self.logged_in,
                                        encoding='utf-8')

    def logged_in(self, response):

        logr.debug("Parsing GitHub logged page Request. Checking whether the login was sucessful")

        PUBLIC = 'public source'
        PRIVATE = 'private source'

        selector = Selector(response)

        successful_login = True if len(selector.xpath(self.login_error_div_xpath).extract()) == 1 else False

        if not successful_login:
            logr.debug("Login unsucessfull.")

        else:
            logr.debug("Login sucessfull.")

            logr.debug("Gathering the repos's names.")
            # Scraping the public repos.
            for repo in selector.xpath(' | '.join([self.user_repos_xpath.format(type=PUBLIC),
                                       self.user_repos_xpath.format(type=PRIVATE)])):

                loader = ItemLoader(item=GitHubRepositoryItem(), selector=repo)

                loader.default_output_processor = Join()

                # Iterate oer all fields in 'repo_fields' and scrapes each piece of data.
                for field, xpath in self.repo_fields.iteritems():
                    loader.add_xpath(field, xpath)
                loader.add_value('repo_type', repo.xpath('.//@class').extract()[0])
                loader.add_value('repo_user', self.login_form_data['login'])

                item = loader.load_item()

                Log.item_yield(logr, item)
                yield loader.load_item()

        Log.add_footer(logr)