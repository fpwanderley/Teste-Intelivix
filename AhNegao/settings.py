BOT_NAME = 'ahnegao'

SPIDER_MODULES = ['AhNegao.spiders']

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'intelivix',
    'password': 'intelivix',
    'database': 'intelivix',
}

ITEM_PIPELINES = {
    'AhNegao.pipelines.AhNegaoArticlePipeline': 0,
}
