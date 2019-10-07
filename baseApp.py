# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:36:43 2019

@author: Tom
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import _tkinter
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import os
import pandas as pd
import matplotlib.animation as animation
from matplotlib import style
import time
import numpy as np
import subprocess
import configparser
import multiprocessing
import collections

root = tk.Tk()
root.title("Base Application")

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)
SPECIAL_FONT = ("Helvetica", 12, "bold italic")
#s = ttk.Style()
#s.configure('TButton', foreground='green')
px = 40
py = 15
exp = False
style.use("ggplot")

class mainApp(ttk.Notebook):
    
    def __init__(self, parent):
        r"""
        Initialize all the variables 
        """
        ttk.Notebook.__init__(self, parent)
        tk.Tk.iconbitmap(parent, default="battery_icos/Iconsmind-Outline-Battery-100.ico")
        #Control Variables
        self.string = tk.StringVar()
        self.double = tk.DoubleVar()
        self.bool = tk.BooleanVar()
        self.int = tk.IntVar()
        self.figure = Figure()
        self.subplot = self.figure.add_subplot(111)
        self.working_dir = None
        self.data_file_path = None

    def popupmsg(self, msg):
        r"""
        Pop-up message to remind the user something needs to happen
        """
        popup = tk.Tk()
        def leavemini():
            popup.destroy()
        popup.wm_title("!")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command = leavemini)
        B1.pack()
        popup.mainloop()

    def askopenfile(self):
        r"""
        Returns an opened file in read mode.
        Used specifically for loading drainage data
        To Do:
        Make more general
        """
        options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialfile'] = 'myfile.txt'
        options['title'] = 'Open Data File'
    
        if self.working_dir is not None:
            options['initialdir'] = self.working_dir
        loadData = filedialog.askopenfile(mode='r', **options)
        if loadData is not None:
            self.data_file_path = loadData.name
            loadData.close()
            self.load_data(self.data_file_path)

    def askrunscript(self):
        r"""
        Returns an opened file in read mode.
        Used specifically for loading drainage data
        To Do:
        Make more general
        """
        options = {}
        options['defaultextension'] = '.py'
        options['filetypes'] = [('python files', '.py')]
        options['initialfile'] = 'test_ga_net.py'
        options['title'] = 'Select Script To Run'
    
        if self.working_dir is not None:
            options['initialdir'] = self.working_dir
        loadData = filedialog.askopenfile(mode='r', **options)
        if loadData is not None:
            script_path = loadData.name
            print("Running Script " +script_path)
            loadData.close()
            inspect_ga_net(filepath=self.working_dir+'\\ga_net', script=script_path)

    def askdirectory(self):
        r"""
        Returns a selected directoryname.
        """
        directory = filedialog.askdirectory()
        if directory is not None:
            self.working_dir = directory

    def animate(self, i):
        r"""
        Animation function to be run continuosly updating the plot on Page 3
        """
        a = self.subplot
        a.clear()
        if len(self.data)> 0:
            a.plot(self.data[:,0], self.data[:,1], 'go-', label="CSV Data")
            a.legend(bbox_to_anchor=(0,1.02,1,0.102),loc=3, ncol=2, borderaxespad=0)
        a.set_xlabel("X-label")
        a.set_ylabel("Y-label")
        root.update_idletasks()

    def check_load(self, method, **args):
        r"""
        Check some things exist before calling function
        """
        
        if (self.data_file_path is None) or (self.working_dir is None):
            self.popupmsg("Please load a data file and set working directory first")
        else:
            method(**args)

    def load_data(self, filename):
        r"""
        Wrapper for loading csv data
        """
        print(filename)
        self.data = pd.read_csv(filename).to_numpy()
        self.popupmsg("Data Loaded")

    def something(self):
        for i in np.arange(0, 110, 10):
            self.progress["value"] = i
            time.sleep(0.25)
            root.update_idletasks()

    def save_config(self, filename='config.ini'):
        r"""
        This method takes all the control variables and saves them into a
        config file, the function is two-fold:
        """
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'working_dir': str(os.path.normpath(self.working_dir)),
                             'data_file_path': str(os.path.normpath(self.data_file_path))}
        config['pg1'] = {}
        config['pg1']['string'] = str(self.string.get())
            
        config['pg2'] = {}
        config['pg2']['int'] = str(self.int.get()) 
        
        with open(filename, 'w') as configfile:
          config.write(configfile)
    
    def load_config(self, filename='config.ini'):
        r"""
        Load the config file to set the control variables in the GUI
        """
        config = configparser.ConfigParser()
        config.read(filename)
        default = config['DEFAULT']
        self.working_dir = str(default['working_dir'])
        self.data_file_path = str(default['data_file_path'])
        pg1 = config['pg1']
        pg2 = config['pg2']
        self.string.set(pg1['string'])
        self.int.set(pg2['int'])
        root.update_idletasks()

class PageOne(tk.Frame):
    r"""
    Page One
    """
    def __init__(self, parent, controller):
        px = 40
        py = 15
        exp = False
        tk.Frame.__init__(self, parent)
        self.controller = controller
        fill = tk.BOTH
        # String Variable
        string_frame = tk.Frame(self)
        lbl1 = ttk.Label(string_frame, text = "A String")
        lbl1.pack(side=tk.LEFT, fill=fill, expand=exp)
        string_list = ["foo", "bar"]
        controller.string.set(string_list[0])
        drop1 = tk.OptionMenu(string_frame, controller.string, *string_list)
        drop1.pack(side=tk.RIGHT, fill=fill, expand=exp)
        string_frame.pack(fill=fill, padx=px, pady=py)

class PageTwo(tk.Frame):
    r"""
    Page Two
    """
    def __init__(self, parent, controller):
        px = 40
        py = 15
        exp = False
        tk.Frame.__init__(self, parent)
        int_frame = tk.Frame(self)
        # Int Variable
        lbl1 = ttk.Label(int_frame, text = "An Integer")
        lbl1.pack(side=tk.LEFT, fill=tk.BOTH, expand=exp)
        int_scale = tk.Scale(int_frame, from_=1, to=100,
                             variable=controller.int,
                             length=400,
                             orient=tk.HORIZONTAL,
                             resolution=1)
        int_scale.set(20)        
        int_scale.pack(side=tk.RIGHT, fill=tk.BOTH, expand=exp)
        int_frame.pack(fill=tk.X, padx=px, pady=py)

class PageThree(tk.Frame):
    r"""
    Page Three
    """  
    def __init__(self, parent, controller):
        px = 40
        py = 20
        exp=True
        tk.Frame.__init__(self, parent)
        button_frame = tk.Frame(self)
        button1 = ttk.Button(button_frame, text="Do Something",
                             command=lambda: controller.something(),
                             style='TButton')
        button1.pack(side=tk.LEFT, fill=tk.BOTH, expand=exp)
        createToolTip(button1,'This is what will happen when you press me')
        button_frame.pack(fill=tk.X, padx=px, pady=py)
        controller.progress = ttk.Progressbar(self, orient="horizontal",
                                length=200, mode="determinate")
        controller.progress["maximum"] = 100.0
        controller.progress["value"] = 0.0
        controller.progress.pack()
        canvas = FigureCanvasTkAgg(controller.figure, self)
        canvas.draw()
        canvas._tkcanvas.pack(fill=tk.BOTH, expand=exp)
        toolbar_frame=tk.Frame(self)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        toolbar_frame.pack(fill=tk.X, padx=px, pady=py, expand=True)

class ToolTip(object):
    r"""
    Class for handy tips when hovering mouse over fields
    """
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        try:
            # For Mac OS
            tw.tk.call("::tk::unsupported::MacWindowStyle",
                       "style", tw._w,
                       "help", "noActivates")
        except tk.TclError:
            pass
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def createToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


###############################################################################


nb = mainApp(root)
nb.pack(fill='both', expand='yes')

f1 = PageOne(root, nb)
f2 = PageTwo(root, nb)
f3 = PageThree(root, nb)

nb.add(f1, text='Page One')
nb.add(f2, text='Page Two')
nb.add(f3, text='Page Three')


menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Set Directory", command = lambda: nb.askdirectory())
filemenu.add_command(label="Load Data", command = lambda: nb.askopenfile())
filemenu.add_separator()
filemenu.add_command(label="Save Settings", command = lambda: nb.check_load(nb.save_config))
filemenu.add_command(label="Load Settings", command = lambda: nb.load_config())
filemenu.add_separator()
filemenu.add_separator()
filemenu.add_command(label="Exit", command = quit)
testmenu = tk.Menu(menubar, tearoff=0)
testmenu.add_command(label="Run Test", command = lambda: nb.askrunscript())
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Test", menu=testmenu)
tk.Tk.config(root, menu=menubar)

#root.geometry("700x600")
ani = animation.FuncAnimation(fig=nb.figure, func=nb.animate, interval=5000)
nb.mainloop()