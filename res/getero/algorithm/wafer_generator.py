import numpy as np
from res.getero.algorithm.main_cycle_old import process_particles
from res.getero.algorithm.monte_carlo import generate_particles
import time
from tqdm import trange
from res.getero.algorithm.dynamic_profile import give_line_arrays, give_max_y
from res.global_entities.wafer import Wafer


class WaferGenerator:
    def __init__(self, master, multiplier, Si_num):
        self.master = master
        self.wafer = Wafer()
        #self.wafer.generate_pure_wafer(multiplier, Si_num)
        #self.wafer.load("test.zip")
        self.wafer.generate_pure_wafer(multiplier, Si_num)
        #self.wafer.make_half()
        #generate_pure_wafer(self, )
        X, Y = give_line_arrays(self.wafer.border_arr)
        self.wafer.profiles = []
        self.wafer.profiles.append([X, Y])

    def change_plasma_params(self, params):
        n_full = (params["j_ar_plus"]+params["j_cl"]+params["j_cl_plus"])

        self.y_ar_plus = params["j_ar_plus"]/n_full
        self.y_cl = params["j_cl"]/n_full
        self.y_cl_plus = params["j_cl_plus"]/n_full
        self.cell_size = params["cell_size"]

        self.N = n_full*self.wafer.xsize*self.cell_size*params["a_0"]

        self.T_i = params["T_i"]
        self.U_i = params["U_i"]

    def run(self, num_iter, num_per_iter):

        ftime = (num_iter*num_per_iter)/self.N
        print("Full time: ", str(ftime)+" s.")
        self.master.contPanel.progress_bar["maximum"] = num_iter
        self.wafer.old_wif = self.wafer.is_full.copy()
        self.wafer.old_wca = self.wafer.counter_arr.copy()
        self.master.contPanel.style.configure("LabeledProgressbar", text=str(1) + "/" + str(num_iter))
        #print(self.y_ar_plus, self.y_cl, self.y_cl_plus, self.U_i, self.wafer.y0, self.wafer.xsize, num_per_iter, self.T_i)
        #print(np.max(self.wafer.counter_arr))
        #print(np.mean(self.wafer.counter_arr))
        for i in trange(num_iter):

            t1 = time.time()
            curr_num_per_iter = num_per_iter
            if self.wafer.is_half:
                curr_num_per_iter = int(0.5 * curr_num_per_iter)
            params = generate_particles(curr_num_per_iter, self.wafer.xsize, y_ar_plus=self.y_ar_plus, y_cl=self.y_cl,
                                        y_cl_plus=self.y_cl_plus, T_i=self.T_i, T_e=self.U_i, y0=self.wafer.y0)
            t2 = time.time()
            if self.y_cl_plus == 0.0:
                R = 1000
            else:
                R = self.y_cl / self.y_cl_plus
            #print("dfdfdfdfdfdf")

            res, _, _, _, _ = process_particles(self.wafer.counter_arr, self.wafer.is_full, self.wafer.border_arr, params, self.wafer.Si_num, self.wafer.xsize,
                              self.wafer.ysize, R, test=False, do_half=self.wafer.is_half)
            #print("res: ",res)
            #if res is None:
            #    pass
            #else:
            #    np.save("curr_counter_arr.npy",res)
            #    int("fffdf")
            if i % 500 == 0:
                #print("fff1")
                X, Y = give_line_arrays(self.wafer.border_arr)
                #print("fff2")
                self.wafer.profiles.append([X, Y])
            if i % 500 == 0:
                print("Num iter: "+str(i)+" Time: "+str(round(ftime*((i+1)/num_iter),3)))
                #print("fff4")
                y_max = give_max_y(self.wafer.border_arr)
                y_0 = self.wafer.border + self.wafer.mask_height

                depth = (y_max-y_0) * self.cell_size * (10 ** 10)
                #print("Depth: ", depth, " angstrem")
                #print("Speed: "+str(round((60*depth/(ftime*((i+1)/num_iter)))))+" angstrem/min")
                self.master.plotF.replot(i, True)
                self.master.plotF.f.savefig("files/tmp_U"+str(round(self.U_i,1))+"_"+str(i)+".png")
                self.wafer.save("files/wafer_"+str(i)+".zip")
                #self.master.plotF.send_picture()
                #self.wafer.save("test.zip")
                #self.wafer.load("test.zip")
            t3 = time.time()

            self.master.contPanel.progress_var.set(i + 1)
            self.master.contPanel.progress_bar.update()
            self.master.contPanel.style.configure("LabeledProgressbar", text=str(i + 2) + "/" + str(num_iter))

        #self.master.plotF.replot(i)
        self.master.plotF.f.savefig("files/tmp" + "_end" + ".png")
        #master.style.configure("LabeledProgressbar", text="0/0")
        #self.master.contPanel.progress_var.set(0)