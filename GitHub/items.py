# -*- coding: utf-8 -*-

from scrapy import Item, Field


class GitHubRepositoryItem(Item):
    """
        GitHub repository container for the scraped data.
    """
    repo_name = Field()
    repo_type = Field()
    repo_user = Field()
