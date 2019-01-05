import csv
from numpy import inf
from map.maps_interface import Topography


class LandingSite:

    landing_sites_list = []

    def __init__(self, name, location, rank):
        self.uid = len(LandingSite.landing_sites_list)
        self.name = name
        self.location = location
        self.rank = rank

    def cost(self, turn_angle=None):
        if turn_angle is None:
            if self.rank == 0:
                return inf
            else:
                return 1/self.rank
        else:
            pass

    @staticmethod
    def import_sites():
        with open('db/fields_example.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            for line in reader:
                name = line[0]
                lat, lon = float(line[1]), float(line[2])
                ground_height = Topography.get_height_by_coordinate(lat, lon)
                location = (lat, lon, ground_height + 100)
                rank = int(line[3])
                LandingSite.landing_sites_list.append(LandingSite(name, location, rank))

    @staticmethod
    def print_landing_sites():
        for site in LandingSite.landing_sites_list:
            print("")
            print(site.name+": ")
            print("UID: " + str(site.uid))
            print(site.location)
            print(site.location)
            print("cost - " + "{0:.4f}".format(site.cost()))

    @staticmethod
    def num_of_sites():
        return len(LandingSite.landing_sites_list)

