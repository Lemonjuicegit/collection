import logging
import time
from pathlib import Path

def createlog(path):
    logpath_info = Path(path) / "log" / 'info'
    logpath_error = Path(path) / "log" / 'error'
    logpath_warning = Path(path) / "log" / 'warning'
    if not logpath_info.exists():
        logpath_info.mkdir(parents=True)
    if not logpath_error.exists():
        logpath_error.mkdir(parents=True)
    if not logpath_warning.exists():
        logpath_warning.mkdir(parents=True)
           
    logger = logging.getLogger(__name__)
    logger.setLevel('INFO')
    formatter = logging.Formatter("%(asctime)s %(filename)s 第%(lineno)s行: %(message)s")
    
    handler = logging.FileHandler(logpath_info / f"{time.strftime('%Y%m%d', time.gmtime(time.time()))}INFO.log", encoding="utf-8")
    handler.setLevel('INFO')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    handler_err = logging.FileHandler(logpath_error / f"{time.strftime('%Y%m%d', time.gmtime(time.time()))}ERROR.log", encoding="utf-8")
    handler_err.setLevel('ERROR')
    handler_err.setFormatter(formatter)
    logger.addHandler(handler_err)
    
    handler_war = logging.FileHandler(logpath_warning / f"{time.strftime('%Y%m%d', time.gmtime(time.time()))}WARNING.log", encoding="utf-8")
    handler_war.setLevel('WARNING')
    handler_war.setFormatter(formatter)
    logger.addHandler(handler_war)
    
    return logger

