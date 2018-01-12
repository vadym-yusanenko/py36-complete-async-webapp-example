# Standard imports
from datetime import datetime

# Project imports
from settings import DB_CONNECTION

# Third-party imports
from peewee import Model, DateTimeField


class Record(Model):
    created_date = DateTimeField(default=datetime.utcnow)

    class Meta:
        database = DB_CONNECTION
