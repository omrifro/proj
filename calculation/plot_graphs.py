import matplotlib.pyplot as plt
import numpy as np
from calculation.online_range_maximization import maximize_range
from calculation.reachability_envelope import glide_slope_func, calc_v_bounds, calc_opt_trajectory


def plot_glide_ratio_and_velocity(current_loc, environment):
    x = np.linspace(-40, 40, 201)
    r = np.zeros((201, 201))
    v = np.zeros((201, 201))
    i, j = 0, 0
    for w_x in x:
        i = 0
        for w_y in x:
            RE, _, VO, _ = maximize_range(P_A=current_loc, environment=environment, W_XI=w_x, W_YI=w_y, d_Psi_I=np.pi)
            r[i,j] = 1/RE[0]
            v[i, j] = VO[0]
            i += 1
        j += 1

    X, Y = np.meshgrid(x, x)
    plt.figure(figsize=(10, 7), dpi=80)

    plt.subplot(211)
    plt.contour(X, Y, r.T, 16, cmap='cool')
    plt.colorbar()
    plt.title("Glide Ratio")
    plt.grid()

    plt.subplot(212)
    plt.contour(X, Y, v.T, 16, cmap='cool')
    plt.colorbar()
    plt.title("Optimal Velocity")
    plt.grid()

    plt.show()


def plot_glide_ratio_sensitivity(environment):
    x_in = np.linspace(0.1, 60, 201)
    x_cr = np.linspace(10, 60, 201)
    y_in = np.zeros((201, 6))
    y_cr = np.zeros((201, 4))
    r = np.zeros((201, 201))
    v = np.zeros((201, 201))

    j = 0
    plt.figure(figsize=(10, 6), dpi=80)
    plt.subplot(121)
    for w_cr in [10, 20, 25, 30]:
        i = 0
        for v in x_cr:
            RE = glide_slope_func(v, environment, 0, w_cr)
            y_cr[i, j] = (1 / RE)
            i += 1
        plt.plot(x_cr, y_cr[:, j])
    plt.title("Glide Ratio")
    plt.legend(['10', '20', '25', '30'])
    plt.ylim((0, 12))
    plt.grid()

    j = 0
    plt.subplot(122)
    for w_in in [-30, -20, -10, 10, 20, 30]:
        i = 0
        for v in x_in:
            RE = glide_slope_func(v, environment, w_in, 0)
            y_in[i, j] = (1/RE)
            i += 1
        plt.plot(x_in, y_in[:, j])
    plt.title("Glide Ratio")
    plt.legend(['-30', '-20', '-10', '10', '20', '30'])
    plt.ylim((0, 25))
    plt.grid()
    plt.show()


def plot_v_bounds(environment):
    lower_bnd_0, opt_0, upper_bnd_0 = [], [], []
    lower_bnd_1, opt_1, upper_bnd_1 = [], [], []
    for w in range(-50, 50):
        l, h = calc_v_bounds(environment.V_0, w, 0)
        opt_0.append(calc_opt_trajectory(w, 0, environment.V_0, l, h))
        lower_bnd_0.append(l * environment.V_0)
        upper_bnd_0.append(h * environment.V_0)

        l, h = calc_v_bounds(environment.V_0, 0, w)
        opt_1.append(calc_opt_trajectory(0, w, environment.V_0, l, h))
        lower_bnd_1.append(l * environment.V_0)
        upper_bnd_1.append(h * environment.V_0)

    plt.figure(figsize=(6, 8), dpi=80)
    plt.subplot(211)
    plt.title("In-Plane wind")
    plt.plot(range(-50, 50), lower_bnd_0, 'g-')
    plt.plot(range(-50, 50), opt_0, 'b')
    plt.plot(range(-50, 50), upper_bnd_0, 'r')
    plt.legend(['Lower bound', 'Optimal', 'Upper bound'])
    plt.grid()

    plt.subplot(212)
    plt.title("Cross-Plane wind")
    plt.plot(range(-50, 50), lower_bnd_1, 'g-')
    plt.plot(range(-50, 50), opt_1, 'b')
    plt.plot(range(-50, 50), upper_bnd_1, 'r')
    plt.legend(['Lower bound', 'Optimal', 'Upper bound'])
    plt.grid()

    plt.show()

