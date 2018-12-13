landing_sites_list = []


class LandingSite:

    num_of_sites = 0

    def __init__(self, name, lon, lat, altitude, priority):
        self.uid = LandingSite.num_of_sites
        self.name = name
        self.latitude = lat
        self.longitude = lon
        self.altitude = altitude
        self.priority = priority
        LandingSite.num_of_sites += 1

    def lon(self):
        return self.longitude

    def lat(self):
        return self.latitude

