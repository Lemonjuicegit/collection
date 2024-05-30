import json

class Config:
    def __init__(self) -> None:
        with open(r'E:\exploitation\collection\server\menuitemURL.json', 'r',encoding='utf-8') as f:
            self.menuitemURL = json.loads(f.read())
        with open(r"E:\exploitation\collection\server\config.json", 'r',encoding='utf-8') as f:
            self.config = json.loads(f.read())

config = Config()
    