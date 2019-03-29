from numpy import sin, cos, arctan, pi, sqrt, linspace, argmin
from scipy.optimize import fsolve



def calc_reach_env(environment, W_XI, W_YI, d_Psi_I):
    Psi_i = 0
    V_opt, Psi_opt, RE, lower, upper = [], [], [], [], []

    while Psi_i < 2*pi:
        W_inplane, W_cross = calc_wind_projection(Psi_i, W_XI, W_YI)
        V_l, V_u = calc_v_bounds(environment.V_0, W_inplane, W_cross)
        V_opt.append(calc_opt_trajectory(W_inplane, W_cross, environment.V_0, V_l, V_u))
        Psi_opt.append(calc_psi_equval(Psi_i, W_cross, V_opt[-1]))
        RE.append(glide_slope_func(V_opt[-1], environment, W_inplane, W_cross))
        Psi_i += d_Psi_I

    return RE, V_opt, Psi_opt


def calc_wind_projection(Psi_i, W_XI, W_YI):
    W_inplane = W_YI * cos(Psi_i) - W_XI * sin(Psi_i)
    W_cross = W_XI * cos(Psi_i) + W_YI * sin(Psi_i)
    return W_inplane, W_cross


def eq_36(v, w_inplane, w_cross):
    return (v ** 6) - 1.5 * (w_cross ** 2) * (v ** 4) + 0.5 * w_inplane * sqrt(v ** 2 - w_cross ** 2) *\
           (3 * (v ** 4) - 1) - (v ** 2) + 0.5 * (w_cross ** 2)


def calc_opt_trajectory(W_inplane, W_cross, V_0, V_l, V_u):
    W_inplane /= V_0
    W_cross /= V_0
    """
    low, high = V_l, V_u
    v_star = (low + high) / 2
    th = 0.00001
    while abs(eq_36(v_star, W_inplane, W_cross)):
        if (high - low) < th:
            break
        if eq_36(v_star, W_inplane, W_cross) < 0:
            low = v_star
        else:
            high = v_star
        v_star = (low + high) / 2
    return v_star * V_0
    """
    func = lambda v: (v**6) - 1.5 * (W_cross**2) * (v**4) + 0.5 * W_inplane * sqrt(v**2 - W_cross**2) *\
                     (3 * (v**4) - 1) - (v**2) + 0.5 * (W_cross**2)
    V = fsolve(func, (V_l + V_u) / 2)
    return V[0] * V_0


def glide_slope_func(V, environment, W_inplane, W_cross):
    K_SR = environment.K_SR
    glide_slope = (K_SR*(V**4 + environment.V_0**4))/(V*(sqrt(V**2 - W_cross**2) + W_inplane))
    return glide_slope


def calc_v_bounds(V_0, W_inplane, W_cross):
    W_inplane /= V_0
    W_cross /= V_0
    v_l = sqrt(abs(1.5 * W_cross**2 + 1.125 * W_inplane**2 - 1.5 * W_inplane *
                   sqrt(0.5*W_cross**2 + 0.5625*W_inplane**2)))
    v_u = sqrt(abs(1.5 * W_cross**2 + 1.125 * W_inplane**2 + 1 - 1.5 * W_inplane *
                   sqrt(0.5*W_cross**2 + 0.5625*W_inplane**2 + 1)))

    return max(v_l, 1/(3**(1/4))), max(v_u, 1)


def calc_psi_equval(Psi_i, W_cross, V):
    return Psi_i + arctan(-W_cross / V)
