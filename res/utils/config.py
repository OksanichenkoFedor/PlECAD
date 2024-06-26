import numpy as np
from numba import njit
import numba as nb
from numba.experimental import jitclass

do_njit = True
cache = False
parallel = False

seed = 40
use_seed= False

multiplier = 0.2 # 0.2 примерно топология 180 нм

Si_num = 84
cell_size = 2.5  # nanometers

wafer_plot_num = 0
wafer_plot_types = ["is_cell", "Si", "SiCl", "SiCl2", "SiCl3"]

num_iter = 3100
num_per_iter = 4000


plasma_params = {
    "T_i": 0.12,
    "U_i": 40,
    "j_ar_plus": 1.0280760204181185e+19,
    "j_cl_plus": 7.266449111171571e+19,
    "j_cl": 2.6629180745936804e+22,
    "cell_size": cell_size*(10.0**(-9)),
    "time": 50,
    "a_0": (((1839*28*9.1*10**(-31))/2330)**(1.0/3.0)) #размер одного слоя Si
}