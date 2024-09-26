from sqlmodel import Session, select,delete
from routers.collection.common.engine import engine

session = Session(engine)

class Service:
    
    def __init__(self,DO):
        self.DO = DO

    def insert(self,data):
        print(data)
        session.bulk_insert_mappings(self.DO, data)
        session.commit()
    
    def insert_one(self,data):
        session.add(data)
        session.commit()
    def select_all(self):
        statement = select(self.DO)
        res = session.exec(statement).all()
        return res
    def select(self,row):
        statement = select(self.DO)
        for key,value in row.items():
            statement = statement.where(getattr(self.DO, key) == value)
        res = session.exec(statement).all()
        return res

    def update(self, data):
        session.bulk_update_mappings(self.DO, data)
        session.commit()
            
    def delete(self, ids:list[int]):
        dele = delete(self.DO).where(self.DO.id.in_(ids))
        session.exec(dele)
        session.commit()