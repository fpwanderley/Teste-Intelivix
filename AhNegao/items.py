
from scrapy import Item, Field


class AhNegaoArticleItem(Item):
    """
        Article container for the scraped data.
    """
    title = Field()
    page = Field()
