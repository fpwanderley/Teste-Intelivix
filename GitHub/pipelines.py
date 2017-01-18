# -*- coding: utf-8 -*-

import logging

from sqlalchemy.orm import sessionmaker

from models import db_connect, create_github_repository_tables, GitRepository
from util.utils import Log

# For logging
logr = logging.getLogger('github')


class GitHubRepositoryPipeline(object):
    """
        GitHubRepository pipeline for storing scraped data in the database.
    """

    def __init__(self):
        """
            Initializes database connection and sessionmaker. Creates article table.
        """
        engine = db_connect()
        create_github_repository_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """
            Save articles in the database.
            This method is called for every item pipeline component.
        """

        session = self.Session()

        repo = GitRepository(**item)

        try:
            session.add(repo)
            session.commit()

            Log.model_commited_on_db(logr, item)
        except:
            session.rollback()

            logr.debug("Model was not commited.")
            raise
        finally:
            session.close()

        return item
