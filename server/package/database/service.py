from sqlmodel import Session, select, delete, SQLModel
from .engine import getSession


class Service:
    def __init__(self, DO: SQLModel, session_conf: dict | str):
        self.DO = DO
        self.session_conf = session_conf
        self.initSession()

    def initSession(self):
        if isinstance(self.session_conf, dict):
            self.session: Session = getSession(**self.session_conf)
        elif isinstance(self.session_conf, str):
            self.session = getSession(conf=self.session_conf)

    def insert(self, data):
        self.session.bulk_insert_mappings(self.DO, data)
        self.session.commit()

    def insert_one(self, data):
        self.session.add(data)
        self.session.commit()

    def select_all(self):
        statement = select(self.DO)
        res = self.session.exec(statement).all()
        return res

    def select(self, row):
        statement = select(self.DO)
        for key, value in row.items():
            statement = statement.where(getattr(self.DO, key) == value)
        res = self.session.exec(statement).all()
        return res

    def update(self, data):
        if isinstance(data, dict):
            up_data = self.select({"id": data["id"]})[0]
            for key, value in data.items():
                if key != "id":
                    setattr(up_data, key, value)
        elif isinstance(data, list):
            self.session.bulk_update_mappings(self.DO, data)
        self.session.commit()

    def delete(self, ids: list[int]):
        dele = delete(self.DO).where(self.DO.id.in_(ids))
        self.session.exec(dele)
        self.session.commit()

    def up_fidld(self, before, after, callable, where=None):
        if where:
            statement = self.select(where)
        else:
            statement = self.select_all()
        up_data = []
        for item in statement:
            item_data = {}
            item_data["id"] = item.id
            item_data[after] = callable(dict(item)[before])
            up_data.append(item_data)

        self.update(up_data)
