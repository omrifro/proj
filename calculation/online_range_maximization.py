from numpy import inf
from db.landing_sites import LandingSite
from calculation import reachability_envelope
from map.maps_interface import get_range, get_bearing


def maximize_range(P_A, environment, W_XI, W_YI, d_Psi_I, landing_sites=LandingSite.landing_sites_list):
    chosen_site = None
    min_cost = inf
    site_index = -1
    RE, V_opt, Psi_opt = reachability_envelope.calc_reach_env(environment, W_XI, W_YI, d_Psi_I)
    for site in landing_sites:
        Psi_i, r_0 = calc_psi_and_range(P_A, site.location)
        i = int(Psi_i/d_Psi_I)
        R_max = (P_A[2] - site.location[2])/RE[i]
        if r_0 < R_max:
            current_cost = site.cost()
            if current_cost < min_cost:
                chosen_site = site
                min_cost = current_cost
                site_index = i

    if chosen_site is not None:
        optimal_velocity = V_opt[site_index]
        # return RE, chosen_site, optimal_velocity, Psi_opt[site_index]
        return RE, chosen_site, V_opt, Psi_opt[site_index]
    else:
        #print("Can NOT reach any landing field!!!")
        return RE, None, V_opt, Psi_opt


def calc_psi_and_range(P_A, P_B):
    Psi = get_bearing(P_A, P_B)
    r_0 = get_range(P_A, P_B)
    return Psi, r_0

