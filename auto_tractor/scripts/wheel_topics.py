#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
import math


# Velocities in kmph
rl_vel = 40
rr_vel = 40

# Steering angles in deg
left_steer = 0
right_steer = 0

def main():
    rospy.init_node('wheel_velocity_commander', anonymous=True)

    #Publishers for each wheel
    pub_rl = rospy.Publisher('/rl_velocity/command', Float64, queue_size=10)
    pub_rr = rospy.Publisher('/rr_velocity/command', Float64, queue_size=10)
    pub_ls = rospy.Publisher('/left_steering_position/command', Float64, queue_size=10)
    pub_rs = rospy.Publisher('/right_steering_position/command', Float64, queue_size=10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        rl = rl_vel*0.2777778
        rr = rr_vel*0.2777778
        ls = 0
        rs = 0

        # rospy.loginfo(f"Velocities: FL={fl}, FR={fr}, RL={rl}, RR={rr}")
        pub_rl.publish(Float64(rl))
        pub_rr.publish(Float64(rr))
        pub_ls.publish(Float64(ls))
        pub_rs.publish(Float64(rs))

        rate.sleep()
        
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass