import os

# Конфигурационные параметры для Flask
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Конфигурационные параметры для Elasticsearch
ELASTICSEARCH_HOSTS = ['localhost:9200']
ELASTICSEARCH_INDEX = 'documents'

# Конфигурационные параметры для базы данных
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'my_database')
DATABASE_USER = os.environ.get('DATABASE_USER', 'my_user')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'my_password')

# Строка подключения к базе данных
SQLALCHEMY_DATABASE_URI = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'
