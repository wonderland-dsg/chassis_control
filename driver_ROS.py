#!/usr/bin/env python
 import rospy
 from std_msgs.msg import String

 def callback(data):
     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

 def listener():

     # In ROS, nodes are uniquely named. If two nodes with the same
     # node are launched, the previous one is kicked off. The
     # anonymous=True flag means that rospy will choose a unique
     # name for our 'listener' node so that multiple listeners can
     # run simultaneously.
     rospy.init_node('listener', anonymous=True)

     rospy.Subscriber("chatter", String, callback)

     # spin() simply keeps python from exiting until this node is stopped
     rospy.spin()

 if __name__ == '__main__':
     listener()



#导入geometry_msgs包中的Twist消息类型
class OutAndBack():
    def __init__(self):
        # 节点名称
        rospy.init_node('out_and_back', anonymous=False)
        # 当终端按下Ctrl＋C之后可以终止节点
        rospy.on_shutdown(self.shutdown)
        # 定义在/cmd_vel Topic中发布Twist消息，控制机器人速度
        self.cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rate = 50
        # 设置更新频率为50HZ
        r = rospy.Rate(rate)
        # 线速度
        linear_speed = 0.2
        # 目标距离
        goal_distance = 1.0
        # 到达目标的时间
        linear_duration = goal_distance / linear_speed
        # 角速度 1.0rad/s
        angular_speed = 1.0
        # 转角为Pi(180 degrees)
        goal_angle = pi
        # How long should it take to rotate?
        angular_duration = goal_angle / angular_speed

        # Loop through the two legs of the trip
        for i in range(2):
            # Initialize the movement command
            move_cmd = Twist()

            # Set the forward speed
            move_cmd.linear.x = linear_speed
            # 机器人向前运动，延时一定时间
            ticks = int(linear_duration * rate)
            for t in range(ticks):
                self.cmd_vel.publish(move_cmd)
                r.sleep()

            # 发送一个空的Twist消息是机器人停止
            move_cmd = Twist()
            self.cmd_vel.publish(move_cmd)
            rospy.sleep(1)

            move_cmd.angular.z = angular_speed
            # 机器人开始旋转，延时一定时间使机器人转180度
            ticks = int(goal_angle * rate)
            for t in range(ticks):
                self.cmd_vel.publish(move_cmd)
                r.sleep()

            # 停下来
            move_cmd = Twist()
            self.cmd_vel.publish(move_cmd)
            rospy.sleep(1)

        # 循环两次之后停止
        self.cmd_vel.publish(Twist())

        # 定义 shutdown(self)可以手动停止机器人
    def shutdown(self):
        # Always stop the robot when shutting down the node.
        rospy.loginfo("Stopping the robot...")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        OutAndBack()
    except:
        rospy.loginfo("Out-and-Back node terminated.")


#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

import rospy
#导入最主要的Python for ROS库
from geometry_msgs.msg import Twist
import Serial_KL25Z as serial

def main():
    pass

def control_callback(data):
    linear_speed_x=data.linear.x
    speed_r=data.angular.z
    print "send:",linear_speed_x,"rotation:",speed_r
    serial.sendFloatSpeed(linear_speed_x,0,speed_r)


def control_chasiss():
     # In ROS, nodes are uniquely named. If two nodes with the same
     # node are launched, the previous one is kicked off. The
     # anonymous=True flag means that rospy will choose a unique
     # name for our 'listener' node so that multiple listeners can
     # run simultaneously.
    rospy.init_node('control_chasiss', anonymous=True)

    rospy.Subscriber("cmd_vel", Twist, control_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
