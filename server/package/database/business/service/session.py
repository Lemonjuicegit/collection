from package.database.engine import getSession


conf = {
    "drivers": "postgresql",
    "url": "192.168.2.200",
    "port": 5432,
    "user": "business",
    "password": "JIAyu123456",
    "database": "business",
}

session = getSession(**conf)
