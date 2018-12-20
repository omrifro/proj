from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from PIL import Image
import glob
import matplotlib.pyplot as plt
import numpy as np
from calculation.consts import Coordinate


class Topography:
    # list of 8 elevation maps
    maps = []

    def __init__(self):
        for im in glob.iglob('map/*.tif'):
            if len(self.maps) == 6:
                self.maps.append(np.zeros((3601, 3601)))
            self.maps.append(np.flip(np.array(Image.open(im)), 0))

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


def plot_terrain(map_idx):
    map_array = Topography.maps[map_idx]
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = np.linspace(0, 3600, 3601)
    X, Y = np.meshgrid(x, x)

    ax.plot_surface(X, Y, map_array, cmap=plt.get_cmap('seismic'), linewidth=0, antialiased=False)
    plt.show()

