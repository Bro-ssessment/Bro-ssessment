import os

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', None)
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', None)
POSTGRES_USER = os.environ.get('POSTGRES_USER', None)
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', None)
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'bro')
