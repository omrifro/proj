from numpy import pi
from map import maps_interface
from db.landing_sites import LandingSite
from db import consts
from calculation.online_range_maximization import maximize_range
import ogr


if __name__ == "__main__":

    # Import the map of Israel
    israelMap = maps_interface.Topography()

    # get 3 heights examples
    h1 = israelMap.get_height_by_coordinate(32.736686, 34.953585)   # Megadim
    h2 = israelMap.get_height_by_coordinate(32.729114, 34.999688)   # Beit Oren
    h3 = israelMap.get_height_by_coordinate(32.820611, 35.567141)   # Sea of Galili
    print("Megadim's height: " + str(h1))
    print("Beit Oren's height: " + str(h2))
    print("Sea of Galili's height: " + str(h3))

    # Topography.plot_terrain()
    LandingSite.import_sites()
    LandingSite.print_landing_sites()

    print("\nL = " + str(maps_interface.get_range((32.729114, 34.999688), (32.730842, 35.003858), unit='m')) + " m")
    print("L = " + str(maps_interface.get_range((32.729114, 34.999688), (32.730842, 35.003858), unit='km')) + " km")
    print("Psi = " + str(maps_interface.get_bearing((32.729114, 34.999688), (32.730842, 35.003858), unit='rad')) + " Rad")
    print("Psi = " + str(maps_interface.get_bearing((32.729114, 34.999688), (32.730842, 35.003858), unit='deg')) + " Deg")

    # calculate V0 for this aircraft
    environment = consts.Consts()
    v_0 = environment.V_0
    print("V0 is " + "{0:.3f}".format(maps_interface.mps2knots(v_0)) + " Knots - (" +
          "{0:.3f}".format(maps_interface.mps2kmh(v_0)) + " km/h)")

    # Initial state (example)
    current_loc = (32.775, 35.025, 4000)
    w_x, w_y = 8, 12

    # Find best Landing field
    RE, site_opt, V_opt, Psi_opt = maximize_range(P_A=current_loc, environment=environment, W_XI=w_x, W_YI=w_y, d_Psi_I=(2*pi)/360)
    print("baaaaa")
