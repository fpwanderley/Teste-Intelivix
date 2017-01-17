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


def create_github_repository_tables(engine):
    """
        Creates all tables

    :return:
    """

    # Criando tabelas do módulo GitHub.
    base.metadata.create_all(engine)


class GitRepository(base):

    __tablename__ = 'git_repository'

    id = Column(Integer, primary_key=True)
    repo_name = Column(String)
    repo_type = Column(String)
    repo_user = Column(String)

    def __repr__(self):
        return ("Nome do Repositório: {0}\n"
                "Tipo do Repositório: {1}\n"
                "Usuário logado: {2}\n").format(self.repo_name, self.repo_type, self.repo_user)
