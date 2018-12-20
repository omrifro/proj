import csv
from numpy import inf
from calculation import consts
from map.maps_interface import Topography


class LandingSite:

    num_of_sites = 0
    landing_sites_list = []

    def __init__(self, name, lat, lon, approch_alt, rank):
        self.uid = LandingSite.num_of_sites
        self.name = name
        ground_height = Topography.get_height(lat=lat, lon=lon)
        self.location = consts.Coordinate(lat, lon, ground_height+approch_alt)
        self.rank = rank
        LandingSite.num_of_sites += 1
        LandingSite.landing_sites_list.append(self)

    def cost(self, turn_angle=None):
        if turn_angle is None:
            if self.rank == 0:
                return inf
            else:
                return 1/self.rank
        else:
            pass

    @staticmethod
    def clean_up():
        LandingSite.landing_sites_list.clear()
        LandingSite.num_of_sites = 0
        return


def import_landing_sites():
    with open('db/fields_example.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            LandingSite(line[0], float(line[1]), float(line[2]), int(line[3]), int(line[4]))


def print_landing_sites():
    for site in LandingSite.landing_sites_list:
        print(site.name+": ")
        print("UID: " + str(site.uid))
        site.location.print_loc()
        site.location.print_alt()
        print("cost - " + "{0:.4f}".format(site.cost()))


def delete_landing_sites():
    LandingSite.clean_up()

