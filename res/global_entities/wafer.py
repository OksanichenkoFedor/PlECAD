import numpy as np

from res.getero.algorithm.dynamic_profile import delete_point, create_point
from res.getero.algorithm.dynamic_profile import give_line_arrays

from omegaconf import OmegaConf

from zipfile import ZipFile
import os


class Wafer:
    def __init__(self, multiplier=None, Si_num=84):
        if not (multiplier is None):
            self.generate_pure_wafer(multiplier, Si_num)

    def process_file(self, filename, verbose=0):
        f = open(filename)
        A = f.readlines()
        f.close()
        for line in A[:]:
            line = line.split()
            if len(line) == 3:
                x = int(line[1])
                y = int(line[2])
                self.counter_arr[:, x, y] = np.array([0, 0, 0, 0])
                self.is_full[x, y] = 0
                delete_point(self.border_arr, x, y)
                # time.sleep(0.05)
                if verbose:
                    print("Delete: ", x, y)
                # self.replot()
            elif len(line) == 6:
                prev_x = int(line[1])
                prev_y = int(line[2])
                curr_x = int(line[4])
                curr_y = int(line[5])
                self.counter_arr[:, prev_x, prev_y] = np.array([0, 0, 0, 1])
                self.is_full[prev_x, prev_y] = 1
                create_point(self.border_arr, prev_x, prev_y, curr_x, curr_y)
                if verbose:
                    print("Create: ", prev_x, prev_y, " from: ", curr_x, curr_y)

    def give_part_of_border(self, target_x, target_y, num_one_side_points):
        # ищем начало
        X, Y = np.zeros(2 * num_one_side_points + 1), np.zeros(2 * num_one_side_points + 1)
        X[num_one_side_points] = target_x
        Y[num_one_side_points] = target_y
        start_x, start_y = target_x, target_y
        for i in range(num_one_side_points):
            new_x, new_y = self.border_arr[start_x, start_y, 1], self.border_arr[start_x, start_y, 2]
            if new_x != -1 and new_y != -1:
                start_x, start_y = new_x, new_y
            X[num_one_side_points - (i + 1)] = start_x
            Y[num_one_side_points - (i + 1)] = start_y

        end_x, end_y = target_x, target_y
        for i in range(num_one_side_points):
            new_x, new_y = self.border_arr[end_x, end_y, 3], self.border_arr[end_x, end_y, 4]
            if new_x != -1 and new_y != -1:
                end_x, end_y = new_x, new_y
            X[num_one_side_points + (i + 1)] = end_x
            Y[num_one_side_points + (i + 1)] = end_y

        return X, Y, num_one_side_points

    def give_el_border(self, target_num):
        curr_x, curr_y = self.start_x, self.start_y
        num = 0
        while num < target_num and (curr_x != self.end_x or curr_y != self.end_y):
            curr_x, curr_y = self.border_arr[curr_x, curr_y, 3], self.border_arr[curr_x, curr_y, 4]
            num += 1
        return curr_x, curr_y

    def save(self, filename):
        # print("Start saveing: ",filename)
        cdict = {
            "multiplier": self.multiplier,
            "Si_num": self.Si_num,
            "border": self.border,
            "xsize": self.xsize,
            "ysize": self.ysize,
            "left_area": self.left_area,
            "right_area": self.right_area,
            "mask_height": self.mask_height,
            "y0": self.y0,
            "silicon_size": self.silicon_size,
            "start_x": self.start_x,
            "start_y": self.start_y,
            "end_x": self.end_x,
            "end_y": self.end_y,
            "profiles": self.profiles
        }
        conf = OmegaConf.create(cdict)
        OmegaConf.save(config=conf, f="cdict.yaml")
        np.save("is_full.npy", self.is_full)
        np.save("counter_arr.npy", self.counter_arr)
        np.save("mask.npy", self.mask)
        np.save("border_arr.npy", self.border_arr)
        # np.save("profiles.npy", np.array(self.profiles))

        with ZipFile(filename, 'w') as myzip:
            myzip.write("is_full.npy")
            myzip.write("counter_arr.npy")
            myzip.write("mask.npy")
            myzip.write("border_arr.npy")
            # myzip.write("profiles.npy")
            myzip.write("cdict.yaml")

        os.remove("is_full.npy")
        os.remove("counter_arr.npy")
        os.remove("mask.npy")
        os.remove("border_arr.npy")
        # os.remove("profiles.npy")
        os.remove("cdict.yaml")

        # print("End saveing: ", filename)

    def load(self, filename):
        with ZipFile(filename) as myzip:
            with myzip.open("is_full.npy") as myfile:
                self.is_full = np.load(myfile)
            with myzip.open("counter_arr.npy") as myfile:
                self.counter_arr = np.load(myfile)
            with myzip.open("mask.npy") as myfile:
                self.mask = np.load(myfile)
            with myzip.open("border_arr.npy") as myfile:
                self.border_arr = np.load(myfile)
            # with myzip.open("profiles.npy") as myfile:
            #    self.profiles = list(np.load(myfile))
            with myzip.open("cdict.yaml") as myfile:
                conf = OmegaConf.load(myfile)
        self.multiplier = float(conf.multiplier)
        self.Si_num = int(conf.Si_num)
        self.border = int(conf.border)
        self.xsize = int(conf.xsize)
        self.ysize = int(conf.ysize)
        self.left_area = int(conf.left_area)
        self.right_area = float(conf.right_area)
        self.mask_height = float(conf.mask_height)
        self.y0 = int(conf.y0)
        self.silicon_size = int(conf.silicon_size)
        self.start_x = int(conf.start_x)
        self.start_y = int(conf.start_y)
        self.end_x = int(conf.end_x)
        self.end_y = int(conf.end_y)
        self.profiles = list(conf.profiles)

    def generate_pure_wafer(self, multiplier, Si_num, fill_sicl3=False):

        self.old_wif = []
        self.old_wca = []
        self.profiles = []
        self.multiplier = multiplier
        self.Si_num = Si_num
        self.border = int(500 * self.multiplier)
        self.xsize = int(2000 * self.multiplier)
        self.ysize = int(2400 * self.multiplier)
        self.left_area = int(850 * self.multiplier)
        self.right_area = int(1150 * self.multiplier)
        self.mask_height = int(40 * self.multiplier)
        self.y0 = 0
        self.silicon_size = int(1600 * self.multiplier)
        # print(25*self.silicon_size)
        self.is_full = np.fromfunction(lambda i, j: j >= self.border, (self.xsize, self.ysize), dtype=int).astype(
            int)
        self.counter_arr = self.is_full.copy() * self.Si_num
        self.mask = np.ones((self.xsize, self.ysize))
        self.mask[:, :self.border] = self.mask[:, :self.border] * 0
        self.mask[:,
        self.border + self.mask_height:self.border + self.mask_height + self.silicon_size] = self.mask[:,
                                                                                             self.border + self.mask_height:self.border +
                                                                                                                            self.mask_height + self.silicon_size] * 0
        self.mask[self.left_area:self.right_area, :self.border + self.mask_height + self.silicon_size] = \
            self.mask[self.left_area:self.right_area, :self.border + self.mask_height + self.silicon_size] * 0
        self.is_full = self.mask + self.is_full
        self.counter_arr = np.repeat(
            self.counter_arr.reshape(1, self.counter_arr.shape[0], self.counter_arr.shape[1]),
            4, axis=0)
        self.counter_arr[1] = self.counter_arr[1] * 0
        self.counter_arr[2] = self.counter_arr[2] * 0
        ind = 3
        if fill_sicl3:
            ind = 0
        self.counter_arr[ind] = self.counter_arr[ind] * 0

        self.counter_arr[0] = self.counter_arr[0] - self.mask * self.Si_num
        self.border_arr = np.ones((self.xsize, self.ysize, 5)) * 0.5
        for i in range(self.xsize):
            self.border_arr[i, self.border, 0] = 1.0
            if i == 0:
                self.border_arr[i, self.border, 1:] = [-1, -1, i + 1, self.border]
                self.start_x, self.start_y = i, self.border
            elif i == self.xsize - 1:
                self.border_arr[i, self.border, 1:] = [i - 1, self.border, -1, -1]
                self.end_x, self.end_y = i, self.border
            else:
                self.border_arr[i, self.border, 1:] = [i - 1, self.border, i + 1, self.border]

        self.border_arr[:, :self.border - 0, :] = self.border_arr[:, :self.border - 0, :] * (
            -2.0)
        self.border_arr[:, self.border + 1:, :] = self.border_arr[:, self.border + 1:, :] * (
            0.0)

        self.border_arr = self.border_arr.astype(int)

        self.clear_between_mask()

        X, Y = give_line_arrays(self.border_arr, self.start_x, self.start_y, self.end_x, self.end_y, 1.5, 1.5)
        self.profiles.append([X, Y])

    def clear_between_mask(self):
        for i in range(self.right_area - self.left_area):
            for j in range(self.mask_height):
                delete_point(self.border_arr, i + self.left_area, j + self.border)
                self.counter_arr[:, i + self.left_area, j + self.border] = np.array([0, 0, 0, 0])
                self.is_full[i + self.left_area, j + self.border] = 0
