#!/usr/bin/env python

import rospy
from gazebo_msgs.msg import ModelStates
import time
import math


prev_dist = None
prev_time = None

def callback(data):
    global prev_dist, prev_time

    try:
        # Finding the index of 'auto_tractor'
        index = data.name.index('auto_tractor')
        
        # Extract position
        position = data.pose[index].position
        x = position.x
        y = position.y
        z = position.z

        # Extract current simulated time from ROS
        current_time = time.time()

        # Printing model position
        rospy.loginfo(f"Auto Tractor Position -> x: {x}, y: {y}, z: {z}")
        
        #Calculating distance
        distance = (x**2 + y**2) ** 0.5
        rospy.loginfo(f"Distance from origin: {distance:.2f}")

        # Calculating velocity
        if prev_dist is not None and prev_time is not None:
            d_dist = math.fabs(distance - prev_dist)
            dt = current_time - prev_time

            if dt > 0:
                velocity = d_dist/dt
                rospy.loginfo(f"Velocity:{velocity:.2f} m/s | {velocity*0.227778:.2f} km/h")

        prev_dist = distance
        prev_time = current_time

    except ValueError:
        rospy.logwarn("auto_tractor not found in model_states")

def listener():
    rospy.init_node('tractor_position_listener', anonymous=True)
    rospy.Subscriber("/gazebo/model_states", ModelStates, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
