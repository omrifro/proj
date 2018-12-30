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
            count = 0
            for line in reader:
                if count == 0:
                    self.C_D0 = float(line[0])
                elif count == 1:
                    self.K = float(line[0])
                elif count == 2:
                    self.m = float(line[0])
                elif count == 3:
                    self.S = float(line[0])
                elif count == 4:
                    self.Ro = float(line[0])
                elif count == 5:
                    self.g = float(line[0])
                count += 1
        self.K_SR = (self.Ro * self.S * self.C_D0) / (2 * self.m * self.g)
        self.V_0 = sqrt(((2 * self.m * self.g) / (self.Ro * self.S)) * sqrt(self.K / self.C_D0))

