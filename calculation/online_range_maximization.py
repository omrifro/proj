from numpy import inf
from map.coordinate import heading_str, mps2knots
from db.landing_sites import LandingSite
from calculation import reachability_envelope


def maximize_range(P_A, V_0, W_XI, W_YI, d_Psi_I, landing_sites=LandingSite.landing_sites_list):
    chosen_site = None
    min_cost = inf
    site_index = -1
    RE, V_opt, Psi_opt = reachability_envelope.calc_reach_env(V_0, W_XI, W_YI, d_Psi_I)
    for site in landing_sites:
        Psi_i, r_0 = calc_psi_and_range(P_A, site.location)
        i = int(Psi_i/d_Psi_I)
        R_max = (P_A.alt_diff_to(site.location))/RE[i]
        if r_0 < R_max:
            current_cost = site.cost()
            if current_cost < min_cost:
                chosen_site = site
                min_cost = current_cost
                site_index = i

    if chosen_site is not None:
        landing_site_name = chosen_site.name
        optimal_velocity = V_opt[site_index]
        heading = Psi_opt[site_index]
        print("Best landing site is: " + landing_site_name)
        print("Turn heading " + heading_str(heading) + " at speed of "+"{0:.2f}".format(mps2knots(optimal_velocity)) \
              + " Knots")
        return RE, chosen_site, optimal_velocity, Psi_opt[site_index]
    else:
        print("Can NOT reach any landing field!!!")
        return None, None, None, None


def calc_psi_and_range(P_A, P_B):
    grid_factor = 111800
    Psi = P_A.angle_to(P_B)
    r_0 = P_A.ground_range_to(P_B, factor=grid_factor)
    return Psi, r_0

