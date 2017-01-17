# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from settings import DATABASE


base = declarative_base()


def db_connect():
    """
        Performs the DB connection.

    :return:
    """

    return create_engine(URL(**DATABASE))


def create_ahnegao_article_tables(engine):
    """
        Creates all tables

    :return:
    """

    # Criando tabelas do módulo AhNegao.
    base.metadata.create_all(engine)


class AhNegaoArticleTitles(base):

    __tablename__ = 'ahnegao_articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    page = Column(Integer)

    def __repr__(self):
        return ("Título do Artigo: {0}\n"
                "Página do Artigo: {1}\n\n").format(self.title, self.page)
