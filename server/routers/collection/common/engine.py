from sqlmodel import create_engine, SQLModel
from package.utils import re_json
from fastapiUtils import cwdpath

conf = re_json(rf"{cwdpath}\config.json")

sqlite_file_name = conf["database"]["server"]
server = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(server, connect_args=connect_args)


def craete_table():
    SQLModel.metadata.create_all(engine)
