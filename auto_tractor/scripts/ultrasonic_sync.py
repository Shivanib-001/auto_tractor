#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Range
import tkinter as tk
from tkinter import ttk
import math

def obj_pos(a, b):
    '''a = Distance of object from Sensor 1
    b = Distance of object from Sensor 2'''
    i = (a**2-b**2+(0.52**2))/(2*0.52)
    j=math.sqrt(a**2-i**2)
    x1,y1=1.8,-0.26 #Coordinates of Sensor
    x=x1+j
    y=y1+i
    print(i,j)
    return x,y

class UltrasonicGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultrasonic Sensor Data")
        self.root.configure(bg="#1e1e1e")
        self.root.geometry("400x300")

        self.title_label = tk.Label(root, text="Ultrasonic Sensor Dashboard", bg="#1e1e1e", fg="#00ffff", font=("Segoe UI", 17, "bold"))
        self.title_label.pack(pady=10)

        self.fl_label = tk.Label(root, text="Front Left: --", font=("Segoe UI", 18),bg="#1e1e1e", fg="#00ff00")
        self.fr_label = tk.Label(root, text="Front Right: --", font=("Segoe UI", 18),bg="#1e1e1e", fg="#00ff00")
        self.ml_label = tk.Label(root, text="Middle Left: --", font=("Segoe UI", 18),bg="#1e1e1e", fg="#00ff00")
        self.mr_label = tk.Label(root, text="Middle Right: --", font=("Segoe UI", 18),bg="#1e1e1e", fg="#00ff00")
        self.pos_label = tk.Label(root, text="Point Position: --", font=("Segoe UI", 18),bg="#1e1e1e", fg="#00ff00")

        self.fl_label.pack(pady=5)
        self.fr_label.pack(pady=5)
        self.ml_label.pack(pady=5)
        self.mr_label.pack(pady=5)
        self.pos_label.pack(pady=5)

        self.fl_range = None
        self.fr_range = None

        rospy.init_node('ultrasonic_sync_node', anonymous=True)
        rospy.Subscriber('/ultrasonic_fr', Range, self.callback_fr)
        rospy.Subscriber('/ultrasonic_fl', Range, self.callback_fl)
        rospy.Subscriber('/ultrasonic_ml', Range, self.callback_ml)
        rospy.Subscriber('/ultrasonic_mr', Range, self.callback_mr)
        self.update_gui()
        
    def callback_fl(self, data):
        self.fl_range = data.range
        self.fl_label.config(text=f"Front Left: {data.range:.4f} m")
        self.obj_pos_plot()
        # print(self.fl_range)
    
    def callback_fr(self, data):
        self.fr_range = data.range
        self.fr_label.config(text=f"Front Right: {data.range:.4f} m")
        self.obj_pos_plot()

    def callback_ml(self, data):
        self.ml_label.config(text=f"Middle Left: {data.range:.4f} m")

    def callback_mr(self, data):
        self.mr_label.config(text=f"Middle Right: {data.range:.4f} m")


    def obj_pos_plot(self):
        if self.fl_range is not None and self.fr_range is not None:
            x,y = obj_pos(self.fl_range, self.fr_range)
            self.pos_label.config(text=f"X: {x:.4f}, Y: {y:.4f}")
            print(x,y)

    def update_gui(self):
        if not rospy.is_shutdown():
            self.root.after(100, self.update_gui)

if __name__ == '__main__':
    root = tk.Tk()
    gui = UltrasonicGUI(root)
    root.mainloop()
