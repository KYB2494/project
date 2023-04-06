#!/usr/bin/env python
import rospy
from obstacle_detector.msg import Obstacles
from std_msgs.msg import UInt8

class Obstacle_e_stop():

    def __init__(self):

        self.MODE = rospy.get_param("~mode") # 1 == Radius, 2 == xy plane
        self.R_TH = rospy.get_param("~r_th")
        self.ANGLE_TH = rospy.get_param("~angle_th")
        self.X_TH = rospy.get_param("~x_th")
        self.Y_TH = rospy.get_param("~y_th")

        self.warning = 0
        self.warning_pub = rospy.Publisher("/obstacle_e_stop/warning", UInt8, queue_size = 1)

        self.obstacle_sub = rospy.Subscriber(rospy.get_param("~obstacle_topic", "/obstacles"), Obstacles, self.obstacleCallback, queue_size=1)

        self.rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            
            self.rate.sleep()
    
    def obstacleCallback(self, msg):
        # callback_str = "length : {}".format(len(msg.circles))
        # rospy.loginfo(callback_str)
        self.warning = 0
        for i in range(len(msg.circles)):
            
            if self.MODE == 1:
                if (msg.circles[i].center.x**2 + msg.circles[i].center.y**2) <= self.R_TH:
                    # rospy.loginfo("Warning")
                    self.warning += 1
                # else:
                    # rospy.loginfo("Safe")
            else:
                if 0 <= msg.circles[i].center.x <= self.X_TH  and -self.Y_TH <=msg.circles[i].center.y <= self.Y_TH:
                    # rospy.loginfo("Warning!")
                    self.warning = +1
                    # self.warning_pub.publish(self.warning)
                # else:
                    # rospy.loginfo("Safe!")
                    # self.warning = 0
                    # self.warning_pub.publish(self.warning)
        if self.warning >= 1:
            rospy.loginfo("Warning!")
            self.warning_pub.publish(1)

        else:
            rospy.loginfo("Safe")
            self.warning_pub.publish(0)  

        

if __name__ == '__main__':
    rospy.init_node("obstacle_e_stop", anonymous=True)
    try:

        oes = Obstacle_e_stop()
    except rospy.ROSInterruptException: pass