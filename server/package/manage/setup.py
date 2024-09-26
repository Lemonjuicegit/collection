import json
from pathlib import Path

menuitemURL = Path(Path.cwd()) / 'menuitemURL.json'

def getRouterName():
    menuitem = json.loads(menuitemURL.read_text(encoding='utf-8'))
    routerName = [key for key in menuitem]
    return routerName


if __name__ == '__main__':
    print(getRouterName())