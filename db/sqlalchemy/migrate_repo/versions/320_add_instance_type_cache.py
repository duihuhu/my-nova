from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Integer

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine    
    instance_types = Table('instance_types',meta,autoload=True)
    cache = Column('cache_mb',Integer)
    instance_types.create_column(cache)
