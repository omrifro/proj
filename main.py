from db import landing_sites
from numpy import pi, sqrt, array
from calculation.online_range_maximization import maximize_range
from calculation import consts
from calculation.consts import Coordinate
from map import maps_interface


if __name__ == "__main__":
    maps_interface.Topography()
    landing_sites.import_landing_sites()
    landing_sites.print_landing_sites()
    for i in range(8):
        maps_interface.plot_terrain(i)

    current_loc = Coordinate(32.500000, 34.764000, 6000)
    h = maps_interface.Topography.get_height(current_loc)
    w_x, w_y = 8, 15
    v_0 = sqrt(((2 * consts.m * consts.g)/(consts.Ro * consts.S))*sqrt(consts.K / consts.C_D0))
    print("V0 is " + "{0:.3f}".format(consts.mps2knots(v_0)) + " Knots - (" + "{0:.3f}".format(consts.mps2kmh(v_0)) + " km/h)")
    angle_steps = (2*pi)/360
    A, B, C, D = maximize_range(P_A=current_loc, V_0=v_0, W_XI=w_x, W_YI=w_y, d_Psi_I=angle_steps)

    landing_sites.delete_landing_sites()

