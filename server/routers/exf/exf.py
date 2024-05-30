from pathlib import Path
import geopandas as gpd
import os,json


def exf(gdb,template_zd,template_fw,savepath):
    with open(template_zd, 'r') as f:
        zd = f.read().split('\n')
    with open(template_fw, 'r') as f:
        fw = f.read().split('\n')
    gdf_zd = gpd.read_file(gdb,layer='宗地')
    gdf_fw = gpd.read_file(gdb,layer='房屋')
    
    def zd_exf(row):
        xy = row.geometry.geoms[0].exterior.xy
        xy_str = '\n'.join([f'{x}∴{y}∴100.000000' for x,y in zip(xy[0],xy[1])])
        xy_str = f"{len(xy[0])}\n{xy_str}"
        FID = row['FID'] if row['FID'] else 0.0 
        F_CODE_ID = row['F_CODE_ID'] if row['F_CODE_ID'] else 0.0 
        F_TEMP_CODE = row['F_TEMP_CODE'] if row['F_TEMP_CODE'] else ''
        F_TEMP_NAME = row['F_TEMP_NAME'] if row['F_TEMP_NAME'] else ''
        F_PARCEL_NO = row['F_PARCEL_NO'] if row['F_PARCEL_NO'] else ''
        bdcdyh = row['不动产单元代码'] if row['不动产单元代码'] else ''
        F_UNDER_CORNERID = row['F_UNDER_CORNERID'] if row['F_UNDER_CORNERID'] else 0.0
        F_LOC_CORNERID = row['F_LOC_CORNERID'] if row['F_LOC_CORNERID'] else 0.0
        F_LAND_LOC = row['F_LAND_LOC'] if row['F_LAND_LOC'] else ''
        F_CALCULATE_AREA = row['F_CALCULATE_AREA'] if row['F_CALCULATE_AREA'] else 0.0
        F_CREATE_BY = row['F_CREATE_BY'] if row['F_CREATE_BY'] else ''
        F_CREATE_TIME = row['F_CREATE_TIME'] if row['F_CREATE_TIME'] else ''
        F_MODIFY_BY = row['F_MODIFY_BY'] if row['F_MODIFY_BY'] else ''
        F_MODIFY_TIME = row['F_MODIFY_TIME'] if row['F_MODIFY_TIME'] else ''
        F_MODIFY_CIRCS = row['F_MODIFY_CIRCS'] if row['F_MODIFY_CIRCS'] else 0
        F_INDB_RIGHTBY = row['F_INDB_RIGHTBY'] if row['F_INDB_RIGHTBY'] else ''
        F_SERIAL_NO = row['F_SERIAL_NO'] if row['F_SERIAL_NO'] else ''
        F_INDB_USETYPE = row['F_INDB_USETYPE'] if row['F_INDB_USETYPE'] else ''
        F_PARCEL_NUMBER = row['F_PARCEL_NUMBER'] if row['F_PARCEL_NUMBER'] else ''
        F_COMMENT = row['F_COMMENT'] if row['F_COMMENT'] else ''
        F_LOCKED = row['F_LOCKED'] if row['F_LOCKED'] else 0.0
        F_SITE_ID = row['F_SITE_ID'] if row['F_SITE_ID'] else 0
        F_FLY_LAND = row['F_FLY_LAND'] if row['F_FLY_LAND'] else 0
        F_RIGHT_PRO = row['F_RIGHT_PRO'] if row['F_RIGHT_PRO'] else 0
        F_PARCEL_NO_OLD = row['F_PARCEL_NO_OLD'] if row['F_PARCEL_NO_OLD'] else ''
        CODE = row['CODE'] if row['CODE'] else 0

        arr = f"{FID}∴{F_CODE_ID}∴{F_TEMP_CODE}∴{F_TEMP_NAME}∴{F_PARCEL_NO}∴{bdcdyh}∴{F_UNDER_CORNERID}" + \
            f"∴{F_LOC_CORNERID}∴{F_LAND_LOC}∴{F_CALCULATE_AREA}∴{F_CREATE_BY}∴{F_CREATE_TIME}∴{F_MODIFY_BY}" + \
            f"∴{F_MODIFY_TIME}∴{F_MODIFY_CIRCS}∴{F_INDB_RIGHTBY}∴{F_SERIAL_NO}∴{F_INDB_USETYPE}∴{F_PARCEL_NUMBER}" + \
            f"∴{F_COMMENT}∴{F_LOCKED}∴{F_SITE_ID}∴{F_FLY_LAND}∴{F_RIGHT_PRO}∴{F_PARCEL_NO_OLD}∴1∴{CODE}"
        temp1 = '\n'.join(zd[:1054])
        temp2 = '\n'.join(zd[1054:1094])
        temp3 = '\n'.join(zd[1095:])
        text = f"{temp1}\n{xy_str}\n{temp2}\n{arr}\n{temp3}"
        with open(f"{os.path.join(savepath,f'{bdcdyh}宗地')}.exf",'w') as f:
            f.write(text)
        
    def fw_exf(row):
        xy = row.geometry.geoms[0].exterior.xy
        xy_str = '\n'.join([f'{x}∴{y}∴100.000000' for x,y in zip(xy[0],xy[1])])
        xy_str = f"{len(xy[0])}\n{xy_str}"
        FID = row['FID'] if row['FID'] else ''
        F_CODE_ID = row['F_CODE_ID'] if row['F_CODE_ID'] else ''
        F_TEMP_CODE = row['F_TEMP_CODE'] if row['F_TEMP_CODE'] else ''
        F_TEMP_NAME = row['F_TEMP_NAME'] if row['F_TEMP_NAME'] else ''
        # F_UNDER_CORNERID = row['F_UNDER_CORNERID'] if row['F_UNDER_CORNERID'] else ''
        # F_OBJECT_NAME = row['F_OBJECT_NAME'] if row['F_OBJECT_NAME'] else ''
        # F_PARCEL_ID = row['F_PARCEL_ID'] if row['F_PARCEL_ID'] else ''
        # F_UNDER_PARCEL_NO = row['F_UNDER_PARCEL_NO'] if row['F_UNDER_PARCEL_NO'] else ''
        bdcdydm = row['不动产单元代码'] if row['不动产单元代码'] else ''
        # F_BASE_AREA = row['F_BASE_AREA'] if row['F_BASE_AREA'] else ''
        # F_CALCULATE_AREA = row['F_CALCULATE_AREA'] if row['F_CALCULATE_AREA'] else ''
        # F_CREATE_BY = row['F_CREATE_BY'] if row['F_CREATE_BY'] else ''
        # F_CREATE_TIME = row['F_CREATE_TIME'] if row['F_CREATE_TIME'] else ''
        # F_MODIFY_BY = row['F_MODIFY_BY'] if row['F_MODIFY_BY'] else ''
        # F_MODIFY_TIME = row['F_MODIFY_TIME'] if row['F_MODIFY_TIME'] else ''
        # F_SERIAL_NO = row['F_SERIAL_NO'] if row['F_SERIAL_NO'] else ''
        # F_BUILDING_TYPE = row['F_BUILDING_TYPE'] if row['F_BUILDING_TYPE'] else ''
        # F_BUILDING_STOREY = row['F_BUILDING_STOREY'] if row['F_BUILDING_STOREY'] else ''
        # F_BUILDING_NO = row['F_BUILDING_NO'] if row['F_BUILDING_NO'] else ''
        # F_COMMENT = row['F_COMMENT'] if row['F_COMMENT'] else ''
        # F_LOCKED = row['F_LOCKED'] if row['F_LOCKED'] else ''
        # F_SITE_ID = row['F_SITE_ID'] if row['F_SITE_ID'] else ''
        # F_BLOCK = row['F_BLOCK'] if row['F_BLOCK'] else ''
        # F_BUILDING_NO_OLD = row['F_BUILDING_NO_OLD'] if row['F_BUILDING_NO_OLD'] else ''
        # ID = row['ID'] if row['ID'] else ''
        CODE = row['CODE'] if row['CODE'] else ''
        
        # arr = f"{FID}∴{F_CODE_ID}∴{F_TEMP_CODE}∴{F_TEMP_NAME}∴{F_UNDER_CORNERID}∴{F_OBJECT_NAME}∴{F_PARCEL_ID}" + \
        #     f"∴{F_UNDER_PARCEL_NO}∴{bdcdydm}∴{F_BASE_AREA}∴{F_CALCULATE_AREA}∴{F_CREATE_BY}∴{F_CREATE_TIME}" + \
        #     f"∴{F_MODIFY_BY}∴{F_MODIFY_TIME}∴{F_SERIAL_NO}∴{F_BUILDING_TYPE}∴{F_BUILDING_STOREY}∴{F_BUILDING_NO}" + \
        #     f"∴{F_COMMENT}∴{F_LOCKED}∴{F_SITE_ID}∴{F_BLOCK}∴{F_BUILDING_NO_OLD}∴1∴{CODE}"
        arr = f"{FID}∴{F_CODE_ID}∴{F_TEMP_CODE}∴{F_TEMP_NAME}∴∴∴" + \
            f"∴∴∴∴∴∴" + \
            f"∴∴∴∴∴∴" + \
            f"∴∴∴∴∴∴1∴{CODE}"
        temp1 = '\n'.join(fw[:1054])
        temp2 = '\n'.join(fw[1054:1106])
        temp3 = '\n'.join(fw[1107:])
        text = f"{temp1}\n{xy_str}\n{temp2}\n{arr}\n{temp3}"
        try:
            with open(f"{os.path.join(savepath,f'{bdcdydm}房屋')}.exf",'w') as f:
                f.write(text)
        except:
            pass

    gdf_zd.apply(zd_exf,axis=1)
    gdf_fw.apply(fw_exf,axis=1)
    
def lq_exf(gdb,savepath):
    current = os.path.dirname(__file__)
    with open(Path(current) / 'template' / '林权.exf', 'r',encoding="gb2312") as f:
        zd = f.read().split('\n')
    
    gdf_zd = gpd.read_file(gdb)
    attributetab_path = Path(current) / 'attributetab.json'
    with open(attributetab_path,'r',encoding="utf-8") as f:
        fields = json.loads(f.read())['TGEOC_DJ_PARCEL_5H']['fields']
    if not (gdf_zd.columns - set(fields)):
        return 0,(gdf_zd.columns - set(fields))
    def zd_exf(row):
        xy = row.geometry.geoms[0].exterior.xy
        xy_str = '\n'.join([f'{x}∴{y}∴0.000000' for x,y in zip(xy[0],xy[1])])
        xy_str = f"{len(xy[0])}\n{xy_str}"
        FID = row['FID'] if row['FID'] else 0.0 
        F_CODE_ID = row['F_CODE_ID'] if row['F_CODE_ID'] else 0.0 
        F_TEMP_CODE = row['F_TEMP_CODE'] if row['F_TEMP_CODE'] else ''
        F_TEMP_NAME = row['F_TEMP_NAME'] if row['F_TEMP_NAME'] else ''
        F_PARCEL_NO = row['F_PARCEL_NO'] if row['F_PARCEL_NO'] else ''
        bdcdyh = row['不动产单元代码'] if row['不动产单元代码'] else ''
        F_UNDER_CORNERID = row['F_UNDER_CORNERID'] if row['F_UNDER_CORNERID'] else 0.0
        F_LOC_CORNERID = row['F_LOC_CORNERID'] if row['F_LOC_CORNERID'] else 0.0
        F_LAND_LOC = row['F_LAND_LOC'] if row['F_LAND_LOC'] else ''
        F_CALCULATE_AREA = row['F_CALCULATE_AREA'] if row['F_CALCULATE_AREA'] else 0.0
        F_CREATE_BY = row['F_CREATE_BY'] if row['F_CREATE_BY'] else ''
        F_CREATE_TIME = row['F_CREATE_TIME'] if row['F_CREATE_TIME'] else ''
        F_MODIFY_BY = row['F_MODIFY_BY'] if row['F_MODIFY_BY'] else ''
        F_MODIFY_TIME = row['F_MODIFY_TIME'] if row['F_MODIFY_TIME'] else ''
        F_MODIFY_CIRCS = row['F_MODIFY_CIRCS'] if row['F_MODIFY_CIRCS'] else 0
        F_INDB_RIGHTBY = row['F_INDB_RIGHTBY'] if row['F_INDB_RIGHTBY'] else ''
        F_SERIAL_NO = row['F_SERIAL_NO'] if row['F_SERIAL_NO'] else ''
        F_INDB_USETYPE = row['F_INDB_USETYPE'] if row['F_INDB_USETYPE'] else ''
        F_PARCEL_NUMBER = row['F_PARCEL_NUMBER'] if row['F_PARCEL_NUMBER'] else ''
        F_COMMENT = row['F_COMMENT'] if row['F_COMMENT'] else ''
        F_LOCKED = row['F_LOCKED'] if row['F_LOCKED'] else 0.0
        F_SITE_ID = row['F_SITE_ID'] if row['F_SITE_ID'] else 0
        F_FLY_LAND = row['F_FLY_LAND'] if row['F_FLY_LAND'] else 0
        F_RIGHT_PRO = row['F_RIGHT_PRO'] if row['F_RIGHT_PRO'] else 0
        F_PARCEL_NO_OLD = row['F_PARCEL_NO_OLD'] if row['F_PARCEL_NO_OLD'] else ''
        CODE = row['CODE'] if row['CODE'] else 0
        
        arr = f"{FID}∴{F_CODE_ID}∴{F_TEMP_CODE}∴{F_TEMP_NAME}∴{F_PARCEL_NO}∴{bdcdyh}∴{F_UNDER_CORNERID}" + \
            f"∴{F_LOC_CORNERID}∴{F_LAND_LOC}∴{F_CALCULATE_AREA}∴{F_CREATE_BY}∴{F_CREATE_TIME}∴{F_MODIFY_BY}" + \
            f"∴{F_MODIFY_TIME}∴{F_MODIFY_CIRCS}∴{F_INDB_RIGHTBY}∴{F_SERIAL_NO}∴{F_INDB_USETYPE}∴{F_PARCEL_NUMBER}" + \
            f"∴{F_COMMENT}∴{F_LOCKED}∴{F_SITE_ID}∴{F_FLY_LAND}∴{F_RIGHT_PRO}∴{F_PARCEL_NO_OLD}∴1∴{CODE}"
        temp1 = '\n'.join(zd[:1054])
        temp2 = '\n'.join(zd[1054:1094])
        temp3 = '\n'.join(zd[1095:])
        text = f"{temp1}\n{xy_str}\n{temp2}\n{arr}\n{temp3}"
        with open(f"{os.path.join(savepath,f'{bdcdyh}宗地')}.exf",'w') as f:
            f.write(text)
    
    gdf_zd.apply(zd_exf,axis=1)
    return 0,()
    
if __name__ == '__main__':
    # shp = r'E:\工作文档\其他\戴\分析数据集.gdb'
    # template_zd = r'E:\exploitation\webpython\routers\hc\合川区+宗地+20220517（南屏农机加油站）.exf'
    # template_fw = r'E:\exploitation\webpython\routers\hc\合川区+房屋（XX车库）+中间库.exf'
    # savepath = r'E:\工作文档\其他\合川\数据库\清平镇'
    # exf(shp,template_zd,template_fw,savepath)
    
    gdb = r"E:\工作文档\qita\新建文件夹 (2)\新建个人地理数据库(扣农房)做EXF.gdb"
    
    lq_exf()