#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64

def main():
    rospy.init_node('wheel_effort_commander', anonymous=True)

    #Publishers for each wheel
    pub_fl = rospy.Publisher('/fl_effort/command', Float64, queue_size=10)
    pub_fr = rospy.Publisher('/fr_effort/command', Float64, queue_size=10)
    pub_rl = rospy.Publisher('/rl_effort/command', Float64, queue_size=10)
    pub_rr = rospy.Publisher('/rr_effort/command', Float64, queue_size=10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        fl = 10000.0
        fr = 10000.0
        rl = 10000.0
        rr = 10000.0

        # rospy.loginfo(f"Velocities: FL={fl}, FR={fr}, RL={rl}, RR={rr}")
        pub_fl.publish(Float64(fl))
        pub_fr.publish(Float64(fr))
        pub_rl.publish(Float64(rl))
        pub_rr.publish(Float64(rr))

        rate.sleep()
        
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass