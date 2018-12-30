from numpy import sqrt
import csv


class Consts:

    C_D0 = 0    # Lift and profile drag coefficients
    K = 0       # Induced drag coefficient
    m = 0       # Aircraft’s mass
    S = 0       # Aerodynamic surface
    Ro = 0      # Air-density
    g = 0       # Gravitational force
    K_SR = 0    # ???
    V_0 = 0     # Optimal gliding speed in still air

    def __init__(self):
        with open('db/consts_example.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            self.C_D0 = float(reader[0][0])
            self.K = float(reader[1][0])
            self.m = float(reader[2][0])
            self.S = float(reader[3][0])
            self.Ro = float(reader[4][0])
            self.g = float(reader[5][0])
        self.K_SR = (self.Ro * self.S * self.C_D0) / (2 * self.m * self.g)
        self.V_0 = sqrt(((2 * self.m * self.g) / (self.Ro * self.S)) * sqrt(self.K / self.C_D0))

