import requests,json
import geopandas as gpd
import pandas as pd
from shapely import Polygon,MultiPolygon,LineString,Point

def getURL(shppath,types):
    if isinstance(shppath,MultiPolygon):
        por = shppath.geoms[0]
    else:
        por = shppath
    xy = list(zip(por.exterior.xy[0],por.exterior.xy[1]))
    xy = [f"{round(v[0],6)},{round(v[1],6)}" for v in xy]
    coordinateStr = '|'.join(xy)
    types_str = '|'.join(types)
    url = f"https://restapi.amap.com/v3/place/polygon?polygon={coordinateStr}&key=c09c99c9d77160b95d1931026eb0d14f&types={types_str}"
    return url

def getPlaceData(url):
    res = requests.get(url,timeout=20)
    res = json.loads(res.content)
    fields = ["address","pname","biz_type","cityname","type","photos","typecode","shopinfo","adname","name","location","tel","id","geometry"]
    gdf = gpd.GeoDataFrame(columns=fields,crs="EPSG:4490")
    temp = {}
    for v in res['pois']:
        temp = v
        temp['photos'] = [p["url"] for p in v["photos"]]
        point = Point(*v['location'].split(","))
        gdf.loc[len(gdf)] = [*[str(temp[key]) for key in fields[:-1]],point]
    return gdf
    
    
def getPlaceData_cll(shppath,types,save):
    gdf = gpd.read_file(shppath)
    res_gdf = None
    for _,row in gdf.iterrows():
        url = getURL(row.geometry,types)
        temp = getPlaceData(url)
        if temp.shape[0] == 0:
            continue
        if res_gdf:
            res_gdf = gpd.concat([res_gdf,temp])
        else:
            res_gdf = temp
    name = save.stem
    res_gdf.to_file(save,encoding="gb18030")
    return list(save.parent.glob(f"{name}.*"))
    

if __name__ == '__main__':
    gdf = gpd.read_file(r'E:\工作文档\云阳县城市国土空间监测\新建文件地理数据库.gdb',layer='云阳县城市国土空间监测')
    res = getURL(gdf.geometry.values[0],['060000'])
    
        
        