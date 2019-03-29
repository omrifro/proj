import gdal
import matplotlib.pyplot as plt
import numpy as np
from haversine import haversine
from shapely.geometry import Polygon


class Topography:

    xoff, a, b, yoff, d, e = None, None, None, None, None, None
    map_array = None

    def __init__(self):
        data_set = gdal.Open('map/israel.tif')
        xoff, a, b, yoff, d, e = data_set.GetGeoTransform()
        Topography.xoff, Topography.a, Topography.b = xoff, a, b
        Topography.yoff, Topography.d, Topography.e = yoff, d, e
        Topography.map_array = data_set.ReadAsArray()

    @staticmethod
    def get_height_by_coordinate(xp, yp):
        x, y = Topography.get_index_from_coordinate(xp, yp)
        return Topography.map_array[x][y]

    @staticmethod
    def get_index_from_coordinate(xp, yp):
        xoff, a, b = Topography.xoff, Topography.a, Topography.b
        yoff, d, e = Topography.yoff, Topography.d, Topography.e

        det = a * e - b * d
        x = round((b * (yp - yoff) - e * (xp - xoff)) / det)
        y = round((a * (yoff - yp) + d * (xp - xoff)) / det)

        if x < 0 or y < 0 or x >= Topography.map_array.shape[0] or y >= Topography.map_array.shape[1]:
            exit(-1)
        return x, y

    @staticmethod
    def plot_terrain(location):
        x = np.linspace(0, Topography.map_array.shape[1]-1, Topography.map_array.shape[1])
        y = np.linspace(0, Topography.map_array.shape[0]-1, Topography.map_array.shape[0])
        X, Y = np.meshgrid(x, y)
        levels_list = list(np.linspace(-450, 3000, 70))
        plt.figure(figsize=(6, 10), dpi=80)
        # plt.contourf(X, Y, np.flip(Topography.map_array, axis=0), 25, cmap='nipy_spectral')
        cs = plt.contour(X, Y, np.flip(Topography.map_array, axis=0), levels_list, cmap='nipy_spectral')
        # plot current location
        x, y = Topography.get_index_from_coordinate(location[0], location[1])
        plt.plot(y, Topography.map_array.shape[0] - x, 'ro')
        plt.colorbar()
        plt.show()

        heights_list = []
        for col in cs.collections:
            # Loop through all polygons that have the same height level
            plt.figure()
            poly_list = []
            for contour_path in col.get_paths():
                # Create the polygon for this intensity level
                # The first polygon in the path is the main one, the following ones are "holes"

                for ncp, cp in enumerate(contour_path.to_polygons()):
                    if len(cp) < 4:
                        continue
                    new_shape = Polygon(cp)
                    if ncp == 0:
                        poly = new_shape
                        poly_list.append(poly)
                        m, n = poly.exterior.xy
                        plt.plot(m, n, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
                    else:
                        # Remove the holes if there are any
                        poly = poly.difference(new_shape)
                        # Can also be left out if you want to include all rings

                # do something with polygon
                plt.show()
            heights_list.append((poly_list, levels_list.pop(0)))


def get_range(src_3d, dst_3d, unit='m'):
    src = tuple([src_3d[0], src_3d[1]])
    dst = tuple([dst_3d[0], dst_3d[1]])
    if len(src_3d) < 3 or len(dst_3d):
        src_alt, dst_alt = 0, 0
    elif src_3d[2] is None or dst_3d[2] is None:
        src_alt, dst_alt = 0, 0
    else:
        src_alt, dst_alt = src_3d[2], dst_3d[2]

    gnd_dist = haversine(src, dst, unit=unit)
    alt_diff = abs(dst_alt - src_alt)

    return np.sqrt(gnd_dist**2 + alt_diff**2)


def get_bearing(src_3d, dst_3d, unit='rad'):
    src = tuple([src_3d[0], src_3d[1]])
    dst = tuple([dst_3d[0], dst_3d[1]])
    rel_pnt = (dst[0], src[1])
    a = get_range(rel_pnt, src)
    b = get_range(rel_pnt, dst)
    if src[0] > dst[0]:
        a = -a
    if src[1] > dst[1]:
        b = -b
    angle = np.arctan2(a, b) % (2 * np.pi)

    if unit is 'deg':
        return np.rad2deg(-angle + np.pi/2) % 360
    else:
        return angle


def mps2knots(speed):
    return 1.94384 * speed


def mps2kmh(speed):
    return 3.6 * speed


def m2ft(height):
    return 3.28084 * height

