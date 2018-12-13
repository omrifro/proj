from numpy import sin, cos, arctan, pi, sqrt, real
from scipy.optimize import fsolve
from calculation import consts


def calc_reach_env(V_0, W_XI, W_YI, d_Psi_I):
    Psi_i = 0
    V_opt, Psi_opt, RE = [], [], []

    while Psi_i < 2*pi:
        W_inplane, W_cross = calc_wind(Psi_i, W_XI, W_YI)
        V_star = calc_V_star(V_0, W_cross)
        V_opt.append(calc_opt_trajectory(W_inplane, W_cross, V_0, V_star))
        Psi_opt.append(Psi_i)
        RE.append(glide_slope_func(V_opt[-1], V_0, W_inplane, W_cross))
        Psi_i += d_Psi_I

    return RE, V_opt, Psi_opt


def calc_wind(Psi_i, W_XI, W_YI):
    W_inplane = W_YI * cos(Psi_i) - W_XI * sin(Psi_i)
    W_cross = W_XI * cos(Psi_i) + W_YI * sin(Psi_i)
    return W_inplane, W_cross


def calc_opt_trajectory(W_inplane, W_cross, V_0, V_star):
    W_inplane -= V_0
    V_b = sqrt(W_cross**2 + min(0, W_inplane)**2)
    v_init = (V_b - V_star)/2
    func = lambda v: v**6 - 1.5*(W_cross**2)*v**4 + 0.5*W_inplane*sqrt(v**2 - W_cross**2)*(3*v**4 - 1) - v**2 + 0.5*W_cross**2
    V = fsolve(func, v_init)
    return real(V) + V_0


def glide_slope_func(V, V_0, W_inplane, W_cross):
    K_SR = (consts.Ro*consts.S*consts.C_D0)/(2*consts.m*consts.g)
    glide_slope = (K_SR*(V**4 + V_0**4))/(V*(sqrt(V**2 - W_cross**2) + W_inplane))
    return glide_slope


def calc_V_star(V_0, W_cross):
    atan_val = ((2*(V_0**2))*sqrt(W_cross**8 + (4/3)*(W_cross**4)*(V_0**4) + (16/27)*(V_0**8)))/(W_cross**6)
    V_star = sqrt(0.5*W_cross**2 + sqrt((4/3)*V_0**4 + W_cross**4)*cos((1/3)*arctan(atan_val)))
    return V_star
