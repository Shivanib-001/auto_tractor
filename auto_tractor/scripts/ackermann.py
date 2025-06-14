#!/usr/bin/env python3

# This node converts cmd_vel inputs to the vehicle to the ROS topics that
# are exposed in Gazebo for moving the vehicle in simulation. Notably, the
# inputs to Gazebo are to joints on the wheel, so there is a multiplier of
# 2.8101 that is applied to the joint's velocity whenever we try to move
# so that the output in Gazebo will match the desired input velocity.

import rospy
from std_msgs.msg import String, Float64
from geometry_msgs.msg import Twist, Pose
import sys, getopt, math

class ackermann:

    def __init__(self,ns):
        self.ns = ns
        rospy.init_node('ackermann', anonymous=True)

        # the format(ns) looks for the namespace in the ros parameter server
        rospy.Subscriber('cmd_vel'.format(ns), Twist, self.callback)

        # Publisher for each controller to publish data
        self.pub_steerL = rospy.Publisher('/left_steering_position/command'.format(ns), Float64, queue_size=1)
        self.pub_steerR = rospy.Publisher('/right_steering_position/command'.format(ns), Float64, queue_size=1)
        self.pub_rearL = rospy.Publisher('/rl_velocity/command'.format(ns), Float64, queue_size=1)
        self.pub_rearR = rospy.Publisher('/rr_velocity/command'.format(ns), Float64, queue_size=1)

        # initial velocity and tire angle are 0
        self.x = 0
        self.z = 0

        # Tractor Wheelbase (in m)
        # simulator value matches the 'real' Tractor
        self.L = 2.264

        # Tractor Track Width
        self.T=1.550

        self.timeout=rospy.Duration.from_sec(0.2);
        self.lastMsg=rospy.Time.now()

        # we want maxsteer to be that of the "inside" tire, and since it is 0.6 in gazebo, we
        # set our ideal steering angle max to be less than that, based on geometry
        self.maxsteerInside=0.6;

        # tan(maxsteerInside) = wheelbase/radius --> solve for max radius at this angle
        rMax = self.L/math.tan(self.maxsteerInside);

        # radius of inside tire is rMax, so radius of the ideal middle tire (rIdeal) is rMax+treadwidth/2
        rIdeal = rMax+(self.T/2.0)

        # tan(angle) = wheelbase/radius
        self.maxsteer=math.atan2(self.L,rIdeal)

        # the ideal max steering angle we can command is now set
        rospy.loginfo(rospy.get_caller_id() + "maximum ideal steering angle set to {0}.".format(self.maxsteer))


    def callback(self,data):
        # 2.6101 is the gain factor in order to account for mechanical reduction of the tyres
        self.x = 2.6101*data.linear.x

        # constrain the ideal steering angle such that the ackermann steering is maxed out
        self.z = max(-self.maxsteer,min(self.maxsteer,data.angular.z))
        self.lastMsg = rospy.Time.now()

    def publish(self):
        # now that these values are published, we
        # reset the velocity, so that if we don't hear new
        # ones for the next timestep that we time out; note
        # that the tire angle will not change

        if self.z != 0:
            T=self.T
            L=self.L

            # self.v is the linear *velocity*
            r = L/math.fabs(math.tan(self.z))

            rL = r-(math.copysign(1,self.z)*(T/2.0))
            rR = r+(math.copysign(1,self.z)*(T/2.0))
            msgRearR = Float64()

            # the right tire will go a little faster when we turn left (positive angle)
            # amount is proportional to the radius of the outside/ideal
            msgRearR.data = self.x*rR/r
            msgRearL = Float64()

            # the left tire will go a little slower when we turn left (positive angle)
            # amount is proportional to the radius of the inside/ideal
            msgRearL.data = self.x*rL/r

            self.pub_rearL.publish(msgRearL)
            self.pub_rearR.publish(msgRearR)

            msgSteerL = Float64()
            msgSteerR = Float64()

            # the left tire's angle is solved directly from geometry
            msgSteerL.data = math.atan2(L,rL)*math.copysign(1,self.z)
            self.pub_steerL.publish(msgSteerL)

            # the right tire's angle is solved directly from geometry
            msgSteerR.data = math.atan2(L,rR)*math.copysign(1,self.z)
            self.pub_steerR.publish(msgSteerR)

        else:
            # if we aren't turning, everything is easy!
            msgRear = Float64()
            msgRear.data = self.x
            self.pub_rearL.publish(msgRear)
            self.pub_rearR.publish(msgRear)

            msgSteer = Float64()
            msgSteer.data = self.z

            self.pub_steerL.publish(msgSteer)
            self.pub_steerR.publish(msgSteer)

def main(argv):
    # we eventually get the ns (namespace) from the ROS parameter server for this node
    ns=''
    node = ackermann(ns)
    rate = rospy.Rate(100) # run at 100Hz
    while not rospy.is_shutdown():
        node.publish()
        rate.sleep()

if __name__ == '__main__':
    main(sys.argv[1:])
