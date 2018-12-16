from db import landing_sites
from numpy import pi, sqrt
from calculation.online_range_maximization import maximize_range
from calculation import consts
from calculation.consts import Coordinate


if __name__ == "__main__":
    landing_sites.import_landing_sites()
    # landing_sites.print_landing_sites()
    current_loc = Coordinate(32.629000, 35.064000, 6000)
    w_x, w_y = 8, 15
    v_0 = sqrt(((2 * consts.m * consts.g)/(consts.Ro * consts.S))*sqrt(consts.K / consts.C_D0))
    print("V0 is " + "{0:.3f}".format(consts.mps2knots(v_0)) + " Knots - (" + "{0:.3f}".format(consts.mps2kmh(v_0)) + " km/h)")
    angle_steps = (2*pi)/360
    A, B, C, D = maximize_range(P_A=current_loc, V_0=v_0, W_XI=w_x, W_YI=w_y, d_Psi_I=angle_steps)

    landing_sites.delete_landing_sites()

