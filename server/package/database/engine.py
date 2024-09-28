from sqlmodel import create_engine, SQLModel, Session
from package.utils import re_json
from fastapiUtils import cwdpath

conf = re_json(rf"{cwdpath}\config.json")

sqlite_file_name = conf["database"]["server"]
server = f"sqlite:///{sqlite_file_name}"


def getEngine(
    drivers=None,
    url=None,
    port=None,
    user=None,
    password=None,
    database=None,
    conf=None,
):
    if conf:
        config = re_json(conf)["database"]
    else:
        config = {
            "drivers": drivers,
            "url": url,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
        }
    match config["drivers"]:
        case "mysql":
            server = f"mysql+pymysql://{config['user']}:{config['password']}@{config['url']}:{config['port']}/{config['database']}"
            return create_engine(server)
        case "sqlite":
            server = f"{config['drivers']}:///{config['server']}"
            connect_args = {"check_same_thread": False}
            return create_engine(server, connect_args=connect_args)
        case "postgresql":
            server = f"postgresql://{config['user']}:{config['password']}@{config['url']}:{config['port']}/{config['database']}"
            return create_engine(server)


def getSession(
    drivers=None,
    url=None,
    port=None,
    user=None,
    password=None,
    database=None,
    conf=None,
):
    return Session(getEngine(drivers, url, port, user, password, database, conf))
