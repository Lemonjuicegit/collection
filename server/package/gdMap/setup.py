from typing import List
import requests,json
import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely import Polygon,MultiPolygon,LineString,Point

gd_key = ["c09c99c9d77160b95d1931026eb0d14f","39ac36d228ade6d9b068ee131785d036"]

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
    gdf = point_poi(res)
    return gdf

def point_poi(poi):
    fields = ["address","pname","biz_type","cityname","type","photos","typecode","shopinfo","adname","name","location","tel","id","geometry"]
    gdf = gpd.GeoDataFrame(columns=fields,crs="EPSG:4490")
    temp = {}
    for v in poi['pois']:
        temp = v
        temp['photos'] = [p["url"] for p in v["photos"]]
        point = Point(*v['location'].split(","))
        gdf.loc[len(gdf)] = [*[str(temp[key]) for key in fields[:-1]],point]
    return gdf        
    
def poi_concat(poi_file_path: List[Path],save):
    res_gdf = None
    for filepath in poi_file_path:
        poi =  json.loads(filepath.read_text(encoding="utf-8"))
        if poi['pois']:
            temp = point_poi(poi)
            if res_gdf:
                res_gdf = gpd.concat([res_gdf,temp])
            else:
                res_gdf = temp
    res_gdf.to_file(save,encoding="gb18030")

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

def geocoding(dz_data,save,save_excel,key):
    df = pd.read_excel(dz_data)
    fields = ["MC","DZ","geometry"]
    gdf = gpd.GeoDataFrame(columns=fields,crs="EPSG:4490")
    data_df = pd.DataFrame(columns=["MC","DZ","X","Y"])
    for _,row in df.iterrows():
        dz_list = row['DZ'].split("、")
        for dz in dz_list:
            url = f"https://restapi.amap.com/v3/geocode/geo?address={dz}&city=重庆&key={gd_key[key]}"
            res = json.loads(requests.get(url,timeout=20).content)
            if res['geocodes']:
                for v in res['geocodes']:
                    x = float(v['location'].split(",")[0])
                    y = float(v['location'].split(",")[1])
                    gdf.loc[len(gdf)] = [row['MC'],row['DZ'],Point(x,y)]
                    data_df.loc[len(data_df)] = [row['MC'],row['DZ'],x,y]
    gdf.to_file(save,encoding="gb18030")
    data_df.to_excel(save_excel)

    
        
        