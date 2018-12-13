from numpy import pi, arctan, sqrt, inf, rad2deg
from calculation import reachability_envelope


def maximize_range(P_A, Z_I, V_0, W_XI, W_YI, d_Psi_I, landing_sites):
    chosen_site = None
    min_cost = inf
    site_index = -1
    RE, V_opt, Psi_opt = reachability_envelope.calc_reach_env(V_0, W_XI, W_YI, d_Psi_I)
    for site in landing_sites:
        Psi_i = calc_psi(P_A, site)
        r_0 = calc_range(P_A, site)
        i = int((Psi_i % 2*pi)/d_Psi_I)
        R_max = (site.altitude - Z_I)/RE[i]
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
        print("Turn heading " + heading + "at speed of "+str(optimal_velocity))
        return RE, chosen_site, optimal_velocity, Psi_opt[site_index]
    else:
        return None


def calc_psi(P_A, P_B):
    N_comp = P_B.lat() - P_A.lat()
    E_comp = P_B.lon() - P_A.lon()
    Psi = arctan(N_comp/E_comp)
    if E_comp < 0:
        Psi += pi
    elif Psi < 0:
        Psi += 2*pi
    return Psi


def calc_range(P_A, P_B):
    grid_factor = 1
    N_comp = P_B.lat() - P_A.lat()
    E_comp = P_B.lon() - P_A.lon()
    r_0 = sqrt(N_comp**2 + E_comp**2)
    return r_0*grid_factor


def calc_heading(Psi):
    deg = rad2deg(Psi)
    deg = round(deg) + 90
    deg %= 360
    heading = str(deg)
    if deg < 10:
        return "00"+heading
    elif deg < 100:
        return "0"+heading
    else:
        return heading


