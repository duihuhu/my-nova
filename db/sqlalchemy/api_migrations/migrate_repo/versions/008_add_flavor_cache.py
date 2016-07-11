from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Integer
from sqlalchemy import Column

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    flavors = Table('flavors', meta, autoload=True)
    cache = Column('cache_mb', Integer)
    flavors.create_column(cache)

