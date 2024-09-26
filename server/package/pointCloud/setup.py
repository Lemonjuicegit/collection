import numpy as np
import geopandas as gpd
import laspy
from shapely.geometry import Point
from pathlib import Path
import dask.array as da
from joblib import Parallel, delayed


def getPointCloudXYZ(las_file: str | Path):
    xyz = np.array([])
    las = laspy.read(las_file)
    for i in range(len(las.x)):
        xyz = np.append(xyz, [las.x[i], las.y[i], las.z[i]])


def las_apply(las_file: str | Path, callback):
    las = laspy.read(las_file)
    for i in range(len(las.x)):
        yield callback([las.x[i], las.y[i], las.z[i]])


def las_density(xyz, gdf):
    point = Point(xyz[0] + 36000000, xyz[1])
    polygon = gdf.loc[0].geometry
    if polygon.contains(point):
        return True
    return False


def dask_apply(data, callback, args):
    dask_array = da.from_array(data)
    lambda_square = lambda x: callback(x, *args)
    vectorized_process_element = np.vectorize(lambda_square)
    result_dask_array = dask_array.map_blocks(vectorized_process_element)
    result_array = result_dask_array.compute()
    return result_array


if __name__ == "__main__":
    is_poi = []
    las_dir = r"E:\工作文档\万州区\水资源\点云"
    files = Path(las_dir).glob("*.las")
    shp = r"E:\工作文档\万州区\鱼背山水库管理线及保护线shp\鱼背山水库.shp"
    gdf = gpd.read_file(shp)
    las = laspy.read(list(files)[2])
    np_xy = np.column_stack((np.array(las.x) + 36000000, np.array(las.y)))

    def eq_poi(xy, shp_gdf):
        if shp_gdf.contains(Point(*xy)):
            return 1
        return 0

    res = Parallel(n_jobs=12)(delayed(eq_poi)(i, gdf.loc[0].geometry) for i in np_xy)

    # res = dask_apply(np_xy, eq_poi, [gdf.loc[0].geometry])
    # contains = las_apply(list(files)[2], lambda x: las_density(x, gdf))
    # for v in contains:
    #     if v:
    #         is_poi.append(v)
    result_array = np.array(res)
    gl = result_array[result_array == 1]
    print(len(gl))
    # density = gdf.area / len(is_poi)
