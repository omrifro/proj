from numpy import pi
from map.maps_interface import Topography
from map import coordinate
from db.landing_sites import LandingSite
from db import consts
from calculation.online_range_maximization import maximize_range


if __name__ == "__main__":
    Topography.import_maps()
    Topography.plot_terrain()
    LandingSite.import_sites()
    LandingSite.print_landing_sites()

    # calculate V0 for this aircraft
    environment = consts.Consts()
    v_0 = environment.V_0
    print("V0 is " + "{0:.3f}".format(coordinate.mps2knots(v_0)) + " Knots - (" +
          "{0:.3f}".format(coordinate.mps2kmh(v_0)) + " km/h)")

    # Initial state (example)
    current_loc = coordinate.Coordinate(32.775, 35.025, 4000)
    w_x, w_y = 8, 12

    # Find best Landing field
    RE, site_opt, V_opt, Psi_opt = maximize_range(P_A=current_loc, environment=environment, W_XI=w_x, W_YI=w_y, d_Psi_I=(2*pi)/1000)

