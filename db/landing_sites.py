landing_sites_list = []


class LandingSite:

    num_of_sites = 0

    def __init__(self, name, lon, lat, altitude, rank):
        self.uid = LandingSite.num_of_sites
        self.name = name
        self.latitude = lat
        self.longitude = lon
        self.altitude = altitude
        self.rank = rank
        LandingSite.num_of_sites += 1

    def lon(self):
        return self.longitude

    def lat(self):
        return self.latitude

    def cost(self):
        return 1/self.rank

