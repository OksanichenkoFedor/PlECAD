import numpy as np
import time
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import tkinter as tk


from res.getero.frontend.grafic_funcs import plot_cells, plot_line, plot_animation
from res.bot.simple import print_message, throw_plot

class Plotter(tk.Frame):
    def __init__(self, parent):
        self.master = parent
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.f = Figure(figsize=(15, 15), dpi=100, tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.f, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, columnspan=2)
        self.canvas.mpl_connect("motion_notify_event", self.move_mouse_event)
        self.canvas.mpl_connect("button_press_event", self.click_mouse_event)
        self.canvas.mpl_connect("button_release_event", self.unclick_mouse_event)

        self.toolbarFrame = tk.Frame(master=self)
        self.toolbarFrame.grid(row=1, columnspan=2, sticky="w")
        self.toolbar1 = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)
        self.ax = self.f.add_subplot(1, 1, 1)
        #self.plot()

    def replot(self, wafer, num=0, do_plot_line=True):
        self.plot_wafer(self.ax, wafer, num, do_plot_line)
        self.canvas.draw()


    def plot_wafer(self, axis, wafer, num=0, do_plot_line=True):
        start = time.time()
        axis.clear()
        axis.set_xlabel('x')
        axis.set_ylabel('y')
        #curr_type = config.wafer_plot_types[config.wafer_plot_num]
        plot_cells(axis, wafer.counter_arr, wafer.is_full, wafer.ysize, wafer.xsize, self.master.wafer_curr_type)
        X, Y = wafer.profiles[-1]
        if do_plot_line:
            plot_line(axis, X, Y, wafer.start_x, wafer.start_y, 0, 0,
                      do_points=False)
        x_major_ticks = np.arange(0, wafer.xsize, 10) + 0.5
        x_minor_ticks = np.arange(0, wafer.xsize, 1) + 0.5
        y_major_ticks = np.arange(0, wafer.ysize, 10) + 0.5
        y_minor_ticks = np.arange(0, wafer.ysize, 1) + 0.5
        axis.set_xticks(x_major_ticks)
        axis.set_xticks(x_minor_ticks, minor=True)
        axis.set_yticks(y_major_ticks)
        axis.set_yticks(y_minor_ticks, minor=True)
        axis.grid(which='minor', alpha=0.2)
        axis.grid(which='major', alpha=0.8)
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)

        plot_animation(wafer.profiles, wafer.xsize, wafer.ysize, num)
        end = time.time()
        print("Plot time: ", round(end-start, 3))

    def send_picture(self, fig):
        fig.savefig("data/pictures/tmp.png")
        throw_plot("data/pictures/tmp.png", 710672679)
        #throw_plot("data/pictures/tmp.gif", 710672679)

    def move_mouse_event(self, event):
        pass

    def click_mouse_event(self, event):
        pass

    def unclick_mouse_event(self, event):
        pass
