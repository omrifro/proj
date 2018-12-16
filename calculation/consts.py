from numpy import sqrt, arctan, pi, rad2deg


C_L, C_D0 = 0, 0.0329       # Lift and profile drag coefficients
D, L = 0, 0                 # Drag and lift force
f, f_0 = 0, 0               # Glide slope function and sink rate function
g_l, g_u = 0, 0             # Optimal velocity Lower and upper bounds auxiliary functions
K = 0.0599                  # Induced drag coefficient
m = 907                     # Aircraft’s mass
n, n_max = 0, 0             # Load factor and maximal load factor
q, q_0 = 0, 0               # Dynamic pressure, optimal dynamic pressure in still air
S = 15.9793                 # Aerodynamic surface
V_MS = 0                    # Minimum sink rate glide velocity
V_stall, V_max = 0, 0       # Aircraft’s stall and maximum velocity
Psi, Psi_max = 0, 0         # The bank angle, maximal bank angle
Ro = 1.25                   # Air-density
g = 9.80665                 # Gravitational force


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
