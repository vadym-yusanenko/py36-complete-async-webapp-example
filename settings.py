# Third-party imports
from peewee_async import PooledPostgresqlDatabase


DB_CONNECTION = PooledPostgresqlDatabase(
    database='awa_db',
    max_connections=1,
    user='awa_user',
    password='awa_pass'
)
