import csv
from sqlmodel import Session, select, delete, SQLModel
from .engine import getSession


class Service:
    def __init__(self, DO: SQLModel, session_conf: dict | str):
        self.DO = DO
        self.session_conf = session_conf
        self.initSession()

    def initSession(self):
        if isinstance(self.session_conf, dict):
            self.session = getSession(**self.session_conf)
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

    def to_csv(self, where=None, file_path=None, encoding="utf-8"):
        if where:
            data = self.select(where)
        else:
            data = self.select_all()
        fields = list(self.DO.__fields__.keys())
        if file_path:
            with open(f"{file_path}.csv", "w", encoding=encoding, newline="") as f:
                write = csv.DictWriter(f, fields)
                write.writeheader()
                write.writerows([v.model_dump() for v in data])
        else:
            with open("data.csv", "w", encoding=encoding, newline="") as f:
                write = csv.DictWriter(f, fields)
                write.writeheader()
                write.writerows([v.model_dump() for v in data])

    def up_fidld(self, before, after, callable, where=None):
        if where:
            statement = self.select(where)
        else:
            statement = self.select_all()
        up_data = []
        for item in statement:
            item_data = {}
            item_data["id"] = item.id
            res = callable(dict(item)[before])
            if res:
                item_data[after] = res
            up_data.append(item_data)

        self.update(up_data)
