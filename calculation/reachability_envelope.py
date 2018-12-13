import numpy as np


def calc_reach_env(V_0, W_i, d_Psi_i):
    Psi_i, i = 0, 0
    V_opt, Psi_opt, RE = [], [], []

    while Psi_i < np.pi:
        W = calc_wind(Psi_i, W_i)
        traj_opt = calc_opt_trajectory(W, V_0)
        # traj_opt is the tuple (V_opt, Psi_opt)
        V_opt.append(traj_opt[0])
        Psi_opt.append(traj_opt[1])
        RE.append(glide_slope_func(V_opt[-1], Psi_opt[-1]))
        Psi_i += d_Psi_i
        i += 1

    return RE, V_opt, Psi_opt


def calc_wind(Psi_i, W_i):
    pass


def calc_opt_trajectory(W, V_0):
    pass


def glide_slope_func(V_opt, Psi_opt):
    pass
