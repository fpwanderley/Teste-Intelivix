# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker

from models import db_connect, create_github_repository_tables, GitRepository


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
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
