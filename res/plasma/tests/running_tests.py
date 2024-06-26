import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
import time

from res.plasma.models.consist_model_aclr import run_consist_model
from res.plasma.models.consist_model_old_consts import run_consist_model as run_consist_model_old
from res.plasma.reactions.consts import e, k_b
from res.plasma.reactions.const_functions import give_consts





N_e = []
N_e_old = []
N_cl = []
N_cl2 = []
N_cl_old = []
N_cl2_old = []
N_ar = []
Beta = []
Beta_old = []
T_e = []
T_e_old = []
plot_arrays = {
    "W_el_Ar": [],
    "W_el_Cl2": [],
    "W_el_Cl": [],
    "W_inel_Ar": [],
    "W_inel_Cl2": [],
    "W_inel_Cl": [],
}

y_ar = np.arange(0.0,1.0,0.01)
Ps = np.arange(0.8,2.0,0.02)*0.13333

Times = []
consts = give_consts("../../data/data.csv", do_rand=False)
run_consist_model(p_0 = 10*0.13333, T_gas = 600, R=0.15, L=0.14, gamma_cl=0.02, y_ar=0.5, W=600, consts=consts)
run_consist_model_old(p_0 = 10*0.13333, T_gas = 600, R=0.15, L=0.14, gamma_cl=0.02, y_ar=0.5, W=600)#, consts=consts)
for i in trange(len(y_ar)):
    curr_y_ar = y_ar[i]
    #print("dfdf: ",curr_y_ar)
    curr_p = 10*0.13333#Ps[i]
    #print(Ps[i])
    start = time.time()
    res = run_consist_model(p_0 = curr_p, T_gas = 600, R=0.15, L=0.14, gamma_cl=0.02, y_ar=curr_y_ar, W=600, consts=consts)
    res_old = run_consist_model_old(p_0=curr_p, T_gas=600, R=0.15, L=0.14, gamma_cl=0.02, y_ar=curr_y_ar, W=600)#, consts=consts)
    end = time.time()
    Times.append(end-start)
    N_e.append(res["n_e"])
    N_e_old.append(res_old["n_e"])
    N_cl.append(res["n_cl"])
    N_cl2.append(res["n_cl2"])
    N_cl_old.append(res_old["n_cl"])
    N_cl2_old.append(res_old["n_cl2"])
    N_ar.append(res["n_ar"])
    T_e.append(res["T_e"])
    T_e_old.append(res_old["T_e"])
    Beta.append(res["n_cl_minus"]/res["n_e"])
    Beta_old.append(res_old["n_cl_minus"] / res_old["n_e"])
    for key in plot_arrays.keys():
        plot_arrays[key].append(res[key])


Times = np.array(Times)
print("Avg time (ms): ",round(1000*Times.mean(),2),"+-",round(1000*Times.std(),2))

fig, ([ax11, ax12], [ax21, ax22]) = plt.subplots(2, 2, figsize=(13, 11))

#fig.suptitle("en_loss first")

ax11.plot(y_ar, np.array(N_e)*(10.0**(-17)), label="Концентрация электронов")
ax11.plot(y_ar, np.array(N_e_old)*(10.0**(-17)), label="Концентрация электронов old")
ax11.set_xlabel("доля аргона",size=10)
ax11.set_ylabel("$n_e, 10^{17} m^{-3}$",size=15)
ax11.set_title("Концентрация электронов")
#ax11.set_ylim([0.5, 1.5])
ax11.grid()
ax11.legend()

ax12.plot(y_ar, np.array(T_e)/(e/k_b), label="T_e")
ax12.plot(y_ar, np.array(T_e_old)/(e/k_b), label="T_e old")
#ax2.plot(y_ar, np.array(T_e_s)/(e/k_b), ".", label="T_e_s")
ax12.set_xlabel("доля аргона",size=10)
ax12.set_ylabel("T_e,eV",size=15)
ax12.set_title("Температура электронов")
#ax12.set_ylim([2.3, 2.8])
ax12.grid()
ax12.legend()


#ax21.plot(y_ar, np.array(N_cl)*(10.0**(-20)),label="new")
#ax21.plot(y_ar, np.array(N_cl_old)*(10.0**(-20)),label="old")
ax21.plot(y_ar, np.array(Beta), label="new")
ax21.plot(y_ar, np.array(Beta_old), label="old")
#ax12.set_title("Потеря энергии на эластичные соударения")
ax21.set_xlabel("доля аргона",size=10)
#ax21.set_ylabel("$n_{Cl}, 10^{20} m^{-3}$",size=15)
ax21.set_title("Концентрация молекул $Cl$")
ax21.set_title("beta")
ax21.grid()
ax21.legend()

ax22.plot(y_ar, np.array(N_cl2)*(10.0**(-19)),label="new")
ax22.plot(y_ar, np.array(N_cl2_old)*(10.0**(-19)),label="old")
#ax12.set_title("Потеря энергии на эластичные соударения")
ax22.set_xlabel("доля аргона",size=10)
ax22.set_ylabel("$n_{Cl_2}, 10^{19} m^{-3}$",size=15)
ax22.set_title("Концентрация молекул $Cl_2$")
ax22.grid()
ax22.legend()

plt.show()


fig, (ax11, ax22) = plt.subplots(1, 2, figsize=(18, 5))



ax22.plot(y_ar, np.array(plot_arrays["W_el_Ar"])*np.array(N_e), label="Ar")
ax22.plot(y_ar, np.array(plot_arrays["W_el_Cl2"])*np.array(N_e), label="Cl2")
ax22.plot(y_ar, np.array(plot_arrays["W_el_Cl"])*np.array(N_e), label="Cl")
ax22.set_title("Потеря энергии на эластичные соударения")
ax22.set_xlabel("доля аргона",size=10)
ax22.set_ylabel("W,Вт",size=15)
ax22.grid()
ax22.legend()

ax11.plot(y_ar, np.array(plot_arrays["W_inel_Ar"])*np.array(N_e), label="Ar")
ax11.plot(y_ar, np.array(plot_arrays["W_inel_Cl2"])*np.array(N_e), label="Cl2")
ax11.plot(y_ar, np.array(plot_arrays["W_inel_Cl"])*np.array(N_e), label="Cl")
ax11.set_title("Потеря энергии на неупругие соударения")
ax11.set_xlabel("доля аргона",size=10)
ax11.set_ylabel("W,Вт",size=15)
ax11.grid()
ax11.legend()

plt.show()