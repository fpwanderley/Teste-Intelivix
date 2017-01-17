# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker

from models import db_connect, create_ahnegao_article_tables, AhNegaoArticleTitles


class AhNegaoArticlePipeline(object):
    """
        AhNegaoArticle pipeline for storing scraped data in the database.
    """

    def __init__(self):
        """
            Initializes database connection and sessionmaker. Creates article table.
        """
        engine = db_connect()
        create_ahnegao_article_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
            Save articles in the database.
            This method is called for every item pipeline component.
        """

        session = self.Session()
        article = AhNegaoArticleTitles(**item)

        try:
            session.add(article)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
