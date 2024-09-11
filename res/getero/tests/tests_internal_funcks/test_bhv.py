from res.global_entities.wafer import Wafer
from res.getero.algorithm.dynamic_profile import delete_point, give_line_arrays
from res.getero.algorithm.ray_tracing.bvh import build_BVH

import res.utils.config as config

import time
import matplotlib.pyplot as plt
import numpy as np

def plot_wafer(c_wafer):
    X, Y = give_line_arrays(c_wafer.border_arr)
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_aspect(1)
    ax.set_ylim([np.array(Y).max(), np.array(Y).min()])
    x_ticks = np.arange(0, c_wafer.xsize, 1)
    y_ticks = np.arange(0, c_wafer.ysize, 1)
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.grid()

    ax.plot(X, Y)
    return ax

def del_some_structure(c_wafer, num_del = 100, seed=10):
    np.random.seed(seed)
    X_del = []
    Y_del = []
    for i in range(num_del):
        X, Y = give_line_arrays(c_wafer.border_arr)
        unfound = True
        while unfound:
            j = np.random.randint(0,len(X))
            curr_x = X[j]
            curr_y = Y[j]
            if c_wafer.is_full[curr_x,curr_y]==1:
                unfound = False
        c_wafer.counter_arr[:, curr_x, curr_y] = np.array([0, 0, 0, 0])
        c_wafer.is_full[curr_x, curr_y] = 0
        delete_point(c_wafer.border_arr, curr_x, curr_y)
        X_del.append(curr_x)
        Y_del.append(curr_y)
    return X_del, Y_del

def plot_rec(curr_axis, NodeList, curr_node, curr_i, i_max):
    print(curr_node)
    left_x, right_x = NodeList[curr_node, 3]-(1.0*i_max-curr_i+0.1)/(1.0*i_max), NodeList[curr_node, 4]+(1.0*i_max-curr_i+0.1)/(1.0*i_max)
    up_y, down_y = NodeList[curr_node, 5]-(1.0*i_max-curr_i+0.1)/(1.0*i_max), NodeList[curr_node, 6]+(1.0*i_max-curr_i+0.1)/(1.0*i_max)
    color = (((1.0*curr_i)/(1.0*i_max)), ((1.0*i_max-1.0*curr_i)/(1.0*i_max)), 0, 0.5+0.5*((1.0*curr_i)/(1.0*i_max)))
    if curr_i==i_max or int(NodeList[curr_node, 1])==-1:
        ax.plot([right_x, right_x],[up_y, down_y], color=color)
        ax.plot([right_x, left_x], [down_y, down_y], color=color)
        ax.plot([left_x, left_x], [down_y, up_y], color=color)
        ax.plot([left_x, right_x], [up_y, up_y], color=color)
    if curr_i<i_max:
        if int(NodeList[curr_node, 1])!=-1:
            plot_rec(curr_axis, NodeList, int(NodeList[curr_node, 1]), curr_i + 1, i_max)
        if int(NodeList[curr_node, 2]) != -1:
            plot_rec(curr_axis, NodeList, int(NodeList[curr_node, 2]), curr_i + 1, i_max)

multiplier, Si_num = 0.01, 84
params = config.plasma_params
test_ray_tracing_params = {
    "mask_height": 200,
    "hole_size": 200,
    "border": 500,
    "xsize": 1000,
    "ysize": 2400,
    "silicon_size": 1600
}
t1 = time.time()
rt_wafer = Wafer()
rt_wafer.generate_pure_wafer(multiplier, Si_num, params=test_ray_tracing_params)
t2 = time.time()
_, _ = del_some_structure(rt_wafer,10, seed=12)
rt_wafer.check_correction()
t3 = time.time()
#X, Y = give_line_arrays(rt_wafer.border_arr)

NodeList = build_BVH(rt_wafer.border_arr)
ax = plot_wafer(rt_wafer)
print(NodeList)
plot_rec(ax, NodeList, 0, 0, 7)
plt.show()
#