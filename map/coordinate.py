from numpy import sqrt, arctan, pi, rad2deg


class Coordinate:
    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def ground_range_to(self, dest, factor=1):
        x = self.lat - dest.lat
        y = self.lon - dest.lon
        return factor * sqrt(x**2 + y**2)

    def alt_diff_to(self, dest):
        return self.alt - dest.alt

    def angle_to(self, dest):
        x = dest.lat - self.lat
        y = dest.lon - self.lon
        theta = arctan(x / y)
        if y < 0:
            theta += pi
        elif theta < 0:
            theta += 2 * pi
        return theta

    def print_loc(self):
        print("<" + str(self.lat) + " N, " + str(self.lon) + " E>")

    def print_alt(self):
        print(str(int(m2ft(self.alt))) + " feet")


def heading_str(angle, units='rad'):
    if units is 'rad':
        deg = int(rad2deg(angle))
    else:
        deg = int(angle)
    deg = (450 - deg) % 360
    heading = str(deg)
    if deg < 10:
        return str("00" + heading)
    elif deg < 100:
        return str("0" + heading)
    else:
        return heading


def mps2knots(speed):
    return 1.94384 * speed


def mps2kmh(speed):
    return 3.6 * speed


def m2ft(height):
    return 3.28084 * height
