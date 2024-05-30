from pathlib import Path
import pandas as pd

class State:
    def __init__(self):
        self.ERR = -1 # 出错状态
        self.GET_READY = 0 # 准备状态
        self.RES = 1 # 执行状态
        self.END = 2 # 结束状态
        self.PONP = 3 # 心跳状态
        
class Store:
    def __init__(self):
        self.useFile:pd.DataFrame = pd.DataFrame(columns=["ip","directory", "filename", "path", "type", "name"])  # coulmns: directory,filename,path,type,name
        self.zipFile = []
        self.uploadPath = Path('\\'.join(__file__.split("\\")[:-2])) / 'upload'
        self.sendPath = Path('\\'.join(__file__.split("\\")[:-2])) / 'send'
    
    def addUseFile(self,ip ,directory:Path,filename: str):
        self.useFile.loc[self.useFile.shape[0]] = [
            ip,
            str(directory/ip),
            filename,
            str(directory/ip / filename),
            filename.split(".")[1],
            filename.split(".")[0],
        ]
    
store = Store()
state = State()