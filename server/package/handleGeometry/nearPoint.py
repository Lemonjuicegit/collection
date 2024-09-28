import math
from pathlib import Path
from typing import Union
import geopandas as gpd
from shapely import Polygon, MultiPolygon


def del_near_point(xy, accuracy):
    count = len(xy)
    extXY = [xy[0]]
    for i in range(1, count - 1):
        mid = xy[i]
        back = xy[i + 1]
        back_distance = math.sqrt((mid[0] - back[0]) ** 2 + (mid[1] - back[1]) ** 2)
        if back_distance >= accuracy:
            extXY.append(mid)
    extXY.append(extXY[0])
    return extXY


def nearPoint(data: Path, accuracy: float, save: Path):
    gdf = gpd.read_file(data)
    delgdf = gpd.GeoDataFrame(columns=gdf.columns)

    def shan(row):
        if type(row.geometry) == MultiPolygon:
            por = row.geometry.geoms[0]
        else:
            por = row.geometry
        xy = list(zip(por.exterior.xy[0], por.exterior.xy[1]))
        extXY = del_near_point(xy, accuracy)
        inner_coords = []
        if por.interiors:
            for lin in por.interiors:
                interiors_xy = list(zip(lin.xy[0], lin.xy[1]))
                interiorsXY = del_near_point(interiors_xy, accuracy)
                inner_coords.append(interiorsXY)
        if inner_coords:
            delgdf.loc[delgdf.shape[0]] = [*row[:-1], Polygon(extXY, inner_coords)]
        else:
            delgdf.loc[delgdf.shape[0]] = [*row[:-1], Polygon(extXY)]

    gdf.apply(shan, axis=1)
    delgdf = delgdf.set_geometry("geometry")
    delgdf.crs = gdf.crs
    delgdf.to_file(save, encoding="gb18030", crs=gdf.crs)
    stem = save.stem

    return sorted(save.parent.glob(f"{stem}.*"))


if __name__ == "__main__":
    datapath = Path(r"E:\工作文档\测试导出数据\删点测试.shp")
    savepath = Path(r"E:\工作文档\测试导出数据\删除点2.shp")
    nearPoint(datapath, 1, savepath)
