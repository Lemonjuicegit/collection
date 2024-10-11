from package.database import BaseService
from fastapiUtils import cwdpath


class Service(BaseService):
    def __init__(self, DO):
        super().__init__(DO, rf"{cwdpath}\config.json")
