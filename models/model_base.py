import sqlalchemy.ext.declarative

ModelBase = sqlalchemy.ext.declarative.declarative_base()
ModelBase.__allow_unmapped__ = True