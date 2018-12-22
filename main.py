from numpy import pi, sqrt, array
from map.maps_interface import Topography
from db.landing_sites import LandingSite
from calculation.online_range_maximization import maximize_range
from calculation import consts
from calculation.consts import Coordinate

if __name__ == "__main__":
    Topography.import_maps()
    Topography.plot_terrain()
    LandingSite.import_sites()
    LandingSite.print_landing_sites()

    # calculate V0 for this aircraft
    v_0 = sqrt(((2 * consts.m * consts.g)/(consts.Ro * consts.S))*sqrt(consts.K / consts.C_D0))
    print("V0 is " + "{0:.3f}".format(consts.mps2knots(v_0)) + " Knots - (" +
          "{0:.3f}".format(consts.mps2kmh(v_0)) + " km/h)")

    # Initial state (example)
    current_loc = Coordinate(32.775, 35.025, 4000)
    w_x, w_y = 8, 12

    # Find best Landing field
    RE, site_opt, V_opt, Psi_opt = maximize_range(P_A=current_loc, V_0=v_0, W_XI=w_x, W_YI=w_y, d_Psi_I=(2*pi)/1000)

