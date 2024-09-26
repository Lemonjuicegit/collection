from math import sqrt,acos,degrees
import geopandas as gpd
from shapely import Polygon,MultiPolygon,LineString

record = r'E:\工作文档\开州项目\新建文件夹\节点比较少.txt'
f = open(record,'a',encoding='gb2312')

def haversine(a,b,c):
    # 计算向量内积
    ab_bc = (b[0]-a[0])*(c[0]-b[0]) + (b[1]-a[1])*(c[1]-b[1])
    # 计算模
    ab = sqrt((b[0]-a[0])**2 + (b[1]-a[1])**2)
    bc = sqrt((c[0]-b[0])**2 + (c[1]-b[1])**2)
    # 计算夹角
    if ab * bc == 0:
        return 0
    cosA = ab_bc / (ab * bc)
    if -1 < cosA < 1:
        theta = acos(ab_bc / (ab * bc))
        return degrees(theta)
    return 0

def sawtooth_xy(xy,por,ignore:int):
    outer_coords = []
    if len(xy) <= ignore:
        return xy,1
    for index,value in enumerate(xy):
        if index == 0:
            front = xy[len(xy)-1]
        else:
            front = xy[index-1]
            
        mid = value
        
        if index == len(xy)-1:
            back = xy[0]
        else:
            back = xy[index+1]
        if 89.9 <= haversine(front,mid,back) <= 90.1:
            lin = gpd.GeoSeries(LineString([front,back]))
            if lin.within(por).values[0]:
                outer_coords.append(mid)
        else:
            outer_coords.append(mid)
    
    return outer_coords,0
        
   
def sawtooth_pol(por,tbbh):
    inner_coords = []
    xy = list(zip(por.exterior.xy[0],por.exterior.xy[1]))
    outer_coords,wbj = sawtooth_xy(xy,por,15)
    if wbj:
        f.write(f"{tbbh}:外边界")
    if por.interiors:
        for lin in por.interiors :
            interiors_xy =  list(zip(lin.xy[0],lin.xy[1]))
            inner,nbj = sawtooth_xy(interiors_xy,por,10)
            inner_coords.append(inner)
            if nbj:
                f.write(f"{tbbh}:内边界")
    if inner_coords:
        return Polygon(outer_coords,inner_coords)

    return Polygon(outer_coords)
             
def sawtooth(shppath,save):
    gdf = gpd.read_file(shppath)
    sawtooth_gdf = gpd.GeoDataFrame(columns=gdf.columns)

    for _,row in gdf.iterrows():
        if isinstance(row.geometry,MultiPolygon):
            por = row.geometry.geoms[0]
        else:
            por = row.geometry
        sawtooth_gdf.loc[sawtooth_gdf.shape[0]] = [*row[:-1],Polygon(sawtooth_pol(por,row.tbbh))]
        yield f"{row.tbbh}完成"
    f.close()
    sawtooth_gdf.to_file(save,encoding="gb18030")

if __name__ == '__main__':
    shp = r"E:\工作文档\开州项目\后备资源.shp"
    savepath = r"E:\工作文档\开州项目\新建文件夹\后备资源.shp"
    res = sawtooth(shp,savepath)
    for v in res:
        print(v)
