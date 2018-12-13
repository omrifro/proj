import csv


class LandingSite:

    num_of_sites = 0
    landing_sites_list = []

    def __init__(self, name, lon, lat, altitude, rank):
        self.uid = LandingSite.num_of_sites
        self.name = name
        self.lat = lat
        self.lon = lon
        self.altitude = altitude
        self.rank = rank
        LandingSite.num_of_sites += 1
        LandingSite.landing_sites_list.append(self)

    def cost(self):
        return 1/self.rank

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
        print("coards - " + str(site.lat)+" N, "+str(site.lon)+" E")
        print("height - " + str(site.altitude))
        print("cost - " + str(site.cost()))
    LandingSite.clean_up()

