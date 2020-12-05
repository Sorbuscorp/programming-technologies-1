from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select
from sqlalchemy.pool import SingletonThreadPool

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
        self.engine=create_engine(connection, connect_args={'check_same_thread': False})
        self.meta=MetaData()        
        self.base=self.engine.connect()

    def addTable(self, tableName, **cols):
        Table(tableName, self.meta)
        for name,Type in cols.items():
            self.meta.tables[tableName].append_column(Column(name,getAlcTypeFromTypename(Type)))
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
            data=self.base.execute(self.meta.tables[tableName].insert(),data)
        except:
            return False
        else:
            return True
        

    def selectAll(self, tableName):
        data = None       
        try:
            data=self.base.execute(select([self.meta.tables[tableName]]))
        except:
            return None
        else:
            return data

    def selectWeatherByLocation(self,location):
        data = None       
        table=self.meta.tables["weather"]
        try:
            data=self.base.execute(select([table]).where(table.c.location==location))
        except:
            return None
        else:
            return data

    def checkDateInBase(self, date, location):
        table=self.meta.tables["weather"]     
        a=self.base.execute(select([table]).where(table.c.date==date and table.c.location==location)).first()
        if a == None:
           return True
        else:
           return False

    def getTables(self):
        return self.meta.tables
