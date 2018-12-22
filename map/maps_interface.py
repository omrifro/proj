from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from PIL import Image
import glob
import matplotlib.pyplot as plt
import numpy as np
from calculation.consts import Coordinate


class Topography:
    # list of 8 elevation maps
    maps = []

    @staticmethod
    def import_maps():
        for im in glob.iglob('map/*.tif'):
            if len(Topography.maps) == 6:
                Topography.maps.append(np.zeros((3601, 3601)))
            Topography.maps.append(np.flip(np.array(Image.open(im)), 0))

    @staticmethod
    def get_height(location=None, lat=0, lon=0):
        # TODO: Implement caching
        if location is None:
            if lat == 0 or lon == 0:
                return np.inf
        else:
            lat = location.lat
            lon = location.lon

        map_idx = get_map_index(lat, lon)
        if map_idx < 0:
            # not in DB range
            return np.inf
        x, y = get_indexes_in_map(lat, lon, map_idx)
        return Topography.maps[map_idx][x, y]

    @staticmethod
    def plot_terrain(map_idx=None):
        if map_idx is None:
            west_half = Topography.maps[0]
            east_half = Topography.maps[1]
            for i in range(3):
                west_half = np.vstack((west_half, Topography.maps[2 * (i+1)]))
                east_half = np.vstack((east_half, Topography.maps[2 * (i + 1) + 1]))
            map_array = np.hstack((west_half, east_half))
            x = np.linspace(0, 3601*2-1, 3601*2)
            y = np.linspace(0, 3601*4-1, 3601*4)
            size = (6, 10)
            c_scale = 25
        else:
            map_array = Topography.maps[map_idx]
            x = np.linspace(0, 3600, 3601)
            y = x
            size = (5, 5)
            c_scale = 40

        X, Y = np.meshgrid(x, y)
        plt.figure(figsize=size, dpi=80)
        plt.contourf(X, Y, map_array, c_scale, cmap='nipy_spectral')
        plt.colorbar()
        plt.show()


def get_indexes_in_map(lat, lon, map_idx):

    if map_idx < 2:
        lat -= 30
    elif map_idx < 4:
        lat -= 31
    elif map_idx < 6:
        lat -= 32
    else:
        lat -= 33

    if not map_idx % 2:
        lon -= 34
    else:
        lon -= 35

    lat_idx = int(lat * 3601)
    lon_inx = int(lon * 3601)

    return lat_idx, lon_inx


def get_map_index(lat, lon):
    # check in range
    if lat < 30 or lat >= 34 or lon < 34 or lon >= 36:
        return -1
    # calc index
    if lat < 31:
        if lon <= 35:
            return 0
        else:
            return 1
    elif lat < 32:
        if lon <= 35:
            return 2
        else:
            return 3
    elif lat < 33:
        if lon <= 35:
            return 4
        else:
            return 5
    else:
        if lon <= 35:
            return 6
        else:
            return 7


