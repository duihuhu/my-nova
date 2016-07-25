from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import String,Integer,DateTime,Boolean
from sqlalchemy import Table

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind=migrate_engine

    columns = [
        (('id',Integer),dict(primary_key=True,nullable=False)),
        (('name',String(255)),dict(nullable=True)),
         (('disabled', Boolean), dict(nullable=True)),
        (('deleted', Boolean), dict(nullable=True)),
        (('created_at', DateTime),dict(nullable=True)),
        (('updated_at', DateTime),dict(nullable=True)),
        (('deleted_at', DateTime),dict(nullable=True))
        ]
    basename = 'policys_provider'
    _columns = tuple([Column(*args,**kwargs) for args,kwargs in columns])
    table = Table(basename,meta,*_columns,mysql_engine='InnoDB',mysql_charset='utf8')
    table.create()
    
def downgrade(migrate_engine):
    pass
