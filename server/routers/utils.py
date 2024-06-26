
import zipfile, os
import pandas as pd

from pathlib import Path
def fileDF(directory_list: list[str]):
    df = pd.DataFrame(columns=["directory", "filename", "path", "type", "name"])
    for directory in directory_list:
        for root, _, files in os.walk(directory):
            if ".gdb" in root:
                continue
            for file in files:
                df.loc[df.shape[0]] = [
                    root,
                    file,
                    Path(root) / file,
                    file.split(".")[1],
                    file.split(".")[0],
                ]
    return df

def unzip(zip_path: str, unzip_path: str,filetype:str=''):
    '''解压文件'''
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        namelist = []
        for info in zip_file.infolist():
            info.filename = info.filename.encode('cp437').decode('gbk')
            namelist.append(info.filename)
            zip_file.extract(info,unzip_path)
        if filetype == 'gdb':
            return zip_path
        return namelist

def zip_list(filelist: list[str|Path], zipname):
    # 多个文件压缩
    with zipfile.ZipFile(zipname, "w") as zip_file:
        for fpath in filelist:
            zip_file.write(fpath, arcname=str(fpath).split(os.sep)[-1])

def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')
 
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()

if __name__ == '__main__':
    cwdpath = Path(r'E:\exploitation\collection\server\send\192.168.2.51')
    pathlist = [cwdpath/'500117031001GB00020F0018房屋.exf',cwdpath/'500117031006GB00008F0001房屋.exf']
    zip_list(pathlist,cwdpath/'测试压缩包.zip')
