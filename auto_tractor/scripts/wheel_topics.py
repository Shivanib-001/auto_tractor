#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64

def main():
    rospy.init_node('wheel_velocity_commander', anonymous=True)

    #Publishers for each wheel
    pub_fl = rospy.Publisher('/fl_velocity/command', Float64, queue_size=10)
    pub_fr = rospy.Publisher('/fr_velocity/command', Float64, queue_size=10)
    pub_rl = rospy.Publisher('/rl_velocity/command', Float64, queue_size=10)
    pub_rr = rospy.Publisher('/rr_velocity/command', Float64, queue_size=10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        v_fl = 10000.0
        v_fr = 10000.0
        v_rl = 10000.0
        v_rr = 10000.0

        pub_fl.publish(Float64(v_fl))
        pub_fr.publish(Float64(v_fr))
        pub_rl.publish(Float64(v_rl))
        pub_rr.publish(Float64(v_rr))

        rate.sleep()
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass