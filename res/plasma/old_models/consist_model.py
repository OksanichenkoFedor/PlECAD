import numpy as np
import matplotlib.pyplot as plt

from res.plasma.consts import e, k_b
from res.plasma.algorithm.electron_temperature import count_T_e
from res.plasma.algorithm.energy_loss import count_n_e
from res.plasma.algorithm.chemical_kinetic import count_simple_start, solve_subsistem_consist, count_ions


def run_consist_model(p_0, T_gas, R, L, gamma_cl, y_ar, W, plot_error=False):
    V = np.pi * R * R * L
    param_vector = (p_0, T_gas, R, L, gamma_cl, y_ar, W, V)
    T_e = 5 * (e / k_b)
    n_e = 1.0 * 10.00 ** (16)

    n_cl_old = None
    delta_n_e = 1
    num = 0
    Deltas = []
    Deltas_cl = []
    Deltas_T_e = []
    Deltas_n_e = []

    k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12, A, B = count_simple_start(T_e, param_vector, do_print=False)

    while (np.abs(delta_n_e) >= 10.0 ** (-15.0)) and (num <= 100):
        num += 1

        n_plus, n_cl2, n_cl, n_cl_minus = solve_subsistem_consist(n_e, k_4, k_5, k_9, k_13, A, do_print=False)

        n_cl_plus, n_cl2_plus, n_ar_plus, n_ar, alphas = count_ions(n_e, n_cl, n_cl_minus, n_plus, B, n_cl2, k_1, k_2,
                                                                    k_3,
                                                                    k_10, k_11, k_12, k_13, do_print=False)

        n_vector = (n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus)

        k_inp = (k_1, k_2, k_3, k_5, k_13)

        k_s, T_e_new = count_T_e(n_vector, param_vector, do_print=False)

        k_1, k_2, k_3, k_4, k_5, k_13, k_9, k_10, k_11, k_12 = k_s

        # cчитаем n_e

        n_e_new = count_n_e(T_e, n_vector, param_vector, do_print=False)

        delta_n_e = (n_e - n_e_new) / (n_e + n_e_new)
        Deltas_n_e.append(np.abs(delta_n_e))
        #print("delta_n_e: ", delta_n_e)
        n_e = n_e_new

        if n_cl_old is None:
            pass
        else:
            delta1 = (n_cl_old - n_cl) / (n_cl_old + n_cl)
            Deltas_cl.append(np.abs(delta1))
            delta_T_e = (T_e - T_e_new) / (T_e + T_e_new)
            Deltas_T_e.append(np.abs(delta_T_e))
        n_cl_old = n_cl
        T_e = T_e_new
    res = {
        "T_e": T_e,
        "n_plus": n_plus,
        "n_e": n_e,
        "n_cl_minus": n_cl_minus,
        "Deltas_T_e": Deltas_T_e,
        "Deltas_n_e": Deltas_n_e
    }

    if plot_error:
        plt.semilogy(Deltas_cl, "o", label="n_cl")
        plt.semilogy(Deltas, ".", label="n_plus")
        plt.semilogy(Deltas_T_e, ".", label="T_e")
        plt.semilogy(Deltas_n_e, ".", label="n_e")
        plt.title("Динамика ошибки от номера итерации")
        plt.grid()
        plt.legend()
        plt.show()
    return res
