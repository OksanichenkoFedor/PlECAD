import numpy as np
from numba import jit

from res.plasma.reactions.consts import k_b, m_cl, m_cl2, m_ar, m_e

#from res.plasma.reactions_consts.Ar import count_Ar_inel_power, give_k_Ar_mom
#from res.plasma.reactions_consts.Cl import count_Cl_inel_power, give_k_Cl_mom
#from res.plasma.reactions_consts.Cl2 import count_Cl2_inel_power, give_k_Cl2_mom
from res.plasma.reactions.reactions_conts import give_k, count_inel_power
from res.plasma.algorithm.utils import count_T_i, count_m_eff, count_tau_eff

@jit(nopython=True)
def count_W_eff(T_e, V, n_ar, n_cl2, n_cl, inel_data, inel_connector, el_data, el_connector, ar_vec, cl2_vec, cl_vec):
    k_ar_m = give_k(el_data[el_connector[30]], T_e)
    k_cl2_m = give_k(el_data[el_connector[14]], T_e)
    k_cl_m = give_k(el_data[el_connector[23]], T_e)
    ar_inel = (V * n_ar * count_inel_power(T_e, inel_data[inel_connector[ar_vec]]))
    cl2_inel = (V * n_cl2 * count_inel_power(T_e, inel_data[inel_connector[cl2_vec]]))
    cl_inel = (V * n_cl * count_inel_power(T_e, inel_data[inel_connector[cl_vec]]))
    inel_part = ar_inel + cl2_inel + cl_inel

    ar_el = (3 * V * T_e * k_b * m_e * k_ar_m * (n_ar / m_ar))
    cl2_el = (3 * V * T_e * k_b * m_e * k_cl2_m * (n_cl2 / m_cl2))
    cl_el = (3 * V * T_e * k_b * m_e * k_cl_m * (n_cl / m_cl))
    el_part = ar_el + cl2_el + cl_el
    return el_part, inel_part, (ar_inel, cl2_inel, cl_inel), (ar_el, cl2_el, cl_el),

@jit(nopython=True)
def count_W_ion(T_e, tau_eff, n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, p_0, T_gas, V):
    T_i = count_T_i(p_0, T_gas)
    m_eff = count_m_eff(n_plus, n_cl2_plus, n_cl_plus, n_ar_plus)
    eU_f = 0.5 * k_b * T_e * np.log((T_e * m_eff) / (T_i * m_e))
    W_ion = (eU_f + 0.5 * T_e * k_b) * tau_eff * V
    return W_ion

@jit(nopython=True)
def count_W_e(T_e, tau_eff, V):
    W_e = 2 * T_e * k_b * tau_eff * V
    return W_e

@jit(nopython=True)
def count_n_e(T_e, n_vector, param_vector, inel_data, inel_connector, el_data, el_connector, ar_vec, cl2_vec, cl_vec):
    p_0, T_gas, R, L, gamma_cl, y_ar, W, V = param_vector
    n_cl, n_cl2, n_ar, n_cl_plus, n_cl2_plus, n_ar_plus, n_plus, n_e, n_cl_minus = n_vector
    tau_eff = count_tau_eff(T_e, n_vector, param_vector)

    W_ion = count_W_ion(T_e, tau_eff, n_plus, n_cl2_plus, n_cl_plus, n_ar_plus, p_0, T_gas, V)
    W_e = count_W_e(T_e, tau_eff, V)
    el_part,inel_part, inel_alphas, el_alphas = count_W_eff(T_e, V, n_ar, n_cl2, n_cl, inel_data, inel_connector,
                                                                                       el_data, el_connector,
                                                                                       ar_vec, cl2_vec, cl_vec)
    W_eff = el_part + inel_part
    n_e = (W - 1 * (W_ion + W_e)) / W_eff
    return n_e, inel_alphas, el_alphas, el_part, inel_part, W_ion, W_e
