import os
from urllib.parse import urlparse
from playhouse import signals
from playhouse.postgres_ext import *


url = urlparse(os.environ["HERMES_DB"])

config = dict(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port,
    sslmode="require",
)

conn = PostgresqlExtDatabase(
    autocommit=True, autorollback=True, register_hstore=False, **config
)


class BaseModel(signals.Model):
    class Meta:
        database = conn


class Users(BaseModel):
    email_address = CharField(primary_key=True)
    username = CharField(null=True)
    password = CharField(null=True)
    date_added = DateTimeField(null=True)
    session_id = CharField(null=True)
    profile_image = CharField(null=True)
    phone = CharField(null=True)


    class Meta:
        db_table = "users"
