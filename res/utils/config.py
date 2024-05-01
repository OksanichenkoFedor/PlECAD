import numpy as np
from numba import njit
import numba as nb
from numba.experimental import jitclass

do_njit = True
cache = False
parallel = False

seed = 40

multiplier = 0.02 # 0.2 примерно топология 180 нм

Si_num = 84
cell_size = 2.5  # nanometers

wafer_plot_num = 0
wafer_plot_types = ["is_cell", "Si", "SiCl", "SiCl2", "SiCl3"]

num_iter = 2500
num_per_iter = 400


plasma_params = {
    "T_i":0.12,
    "T_e":40,
    "y_ar_plus":0.1,
    "y_cl_plus":0.1,
    "y_cl":0.8
}