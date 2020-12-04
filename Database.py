from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select

def getAlcTypeFromTypename(typename):
    typename=typename.lower()
    if  typename == "string":
        return String
    elif typename == "float":
        return Float
    else:
        return None


class Database:

    def __init__(self, connection):
        self.engine=create_engine(connection)
        self.meta=MetaData()
        self.tables={}
        self.base=None

    def addTable(self, tableName, **cols):
        self.tables[tableName]=Table(tableName, self.meta)
        for name,Type in cols.items():
            self.tables[tableName].append_column(Column(name,getAlcTypeFromTypename(Type)))
        pass


    def createBase(self):
        self.meta.create_all(self.engine)
        self.base = self.engine.connect()

    def connect(self):
        self.base = self.engine.connect()
        
    def insert(self, tableName, data):
        if data == None:
            return False
        try:
            data=self.base.execute(self.tables[tableName].insert(),data)
        except:
            return False
        else:
            return True
        

    def select(self, tableName, *columns):
        data = None
        try:
            data=self.base.execute(select([self.tables[tableName]]))
        except:
            return None
        else:
            return data


    def getTables(self):
        return self.tables
