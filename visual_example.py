# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 20:30:49 2019

@author: Tom
"""

import vpython as vs
try:
    # Python2
    import Tkinter as tk
    import thread
except ImportError:
    # Python3
    import tkinter as tk
    import _thread as thread
# will be global
sphere = None
def vthread():
    global sphere
    vs.scene.title = "Sphere in space (3D drag with right mouse button)"
    vs.scene.autoscale = False
    sphere = vs.sphere(pos=(0, 0, 0), color=vs.color.green)
def move_sphere_incr_x(event=None):
    """
    moves along the original x axis incrementing x
    each time the Tkinter b_incr_x button is pressed
    """
    x, y, z = sphere.pos
    sphere.pos = (x+1, y, z)
def move_sphere_decr_x(event=None):
    """
    moves along the original x axis decrementing x
    each time the Tkinter b_decr_x button is pressed
    """
    x, y, z = sphere.pos
    sphere.pos = (x-1, y, z)
root = tk.Tk()
w = 280
h = 150
x = 450
y = 100
# use width x height + x_offset + y_offset (no spaces!)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))
root.title("Control Sphere from here")
b_incr_x = tk.Button(root, text="move right on x axis (increment x)")
# bind passes an event to function
b_incr_x.bind("<Button-1>", move_sphere_incr_x)
b_incr_x.grid(row=0, column=0, padx=20, pady=10)
b_decr_x = tk.Button(root, text="move left on x axis (decrement x)")
# bind passes an event to function
b_decr_x.bind("<Button-1>", move_sphere_decr_x)
b_decr_x.grid(row=1, column=0, padx=10)
# use thread to do run VPython and Tkinter simultaneously
# thread.start_new_thread(function, args)
# args is an empty tuple here
sphere = thread.start_new_thread(vthread, ())
root.mainloop()