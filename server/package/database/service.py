from sqlmodel import select, delete


class Service:
    def __init__(self, DO, session):
        self.DO = DO
        self.session = session

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
        self.session.bulk_update_mappings(self.DO, data)
        self.session.commit()

    def delete(self, ids: list[int]):
        dele = delete(self.DO).where(self.DO.id.in_(ids))
        self.session.exec(dele)
        self.session.commit()
