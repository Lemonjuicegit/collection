from pathlib import Path
from uuid import uuid4
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
        self.useFile:pd.DataFrame = pd.DataFrame(columns=["ip","directory", "filename", "path", "type", "name",'ID'])  # coulmns: directory,filename,path,type,name
        self.zipFile = []
        self.cwdpath = Path.cwd()
        self.uploadPath = Path(self.cwdpath) / 'upload'
        self.sendPath = Path(self.cwdpath) / 'send'
        self.serverip = "183.71.245.98:45454"
    
    def addUseFile(self,ip ,directory:Path,filename: str,ID:str=str(uuid4())):
        """
        Args:
            ip (str): ip地址字符串
            directory (str): 完整的文件路径
            filename (str): 带后缀的文件名
        """
        self.useFile.loc[self.useFile.shape[0]] = [
            ip,
            directory/ip,
            filename,
            directory/ip / filename,
            filename.split(".")[1],
            filename.split(".")[0],
            ID,
        ]
    def drop_query(self,where):
        """删除文件并返回一个空列表"""
        drop_df = self.useFile.query(where)
        def drop_file(path):
            if path.is_dir():
                for i in path.iterdir():
                    drop_file(i)
                path.rmdir()
            else:
                path.unlink()
        drop_df.path.apply(drop_file)  
        self.useFile = self.useFile.drop(drop_df.index)
        return []

    def file_id(self,id,fiedl="all"):
        res = self.useFile[self.useFile.ID == id]
        return self.match_field(res,fiedl)

    def query(self,where,field="all"):
        res = self.useFile.query(where)
        return self.match_field(res,field)
        
    def match_field(self,res,field):
        match field:
            case 'ip':
                return res.ip.values[0]
            case 'directory':
                return res.directory.values[0]
            case 'filename':
                return res.filename.values[0]
            case 'path':
                return res.path.values[0]
            case 'type':
                return res.type.values[0]
            case 'name':
                return res.name.values[0]
            case 'all':
                return res

store = Store()
state = State()
