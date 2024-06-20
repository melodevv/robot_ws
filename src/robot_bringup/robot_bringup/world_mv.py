#!/usr/bin/env python3

import rclpy
import tf2_ros

import tf_transformations
from geometry_msgs.msg import TransformStamped, Twist
from math import sin, cos

robot_yaw = 0.0
robot_x = 0.0
robot_y = 0.0
delta_time = 0.0

def quaternion_from_euler(roll, pitch, yaw):
    #calculate quaternions from euler angles
    quat = tf_transformations.quaternion_from_euler(roll, pitch, yaw)
    t = TransformStamped()
    t.transform.rotation.x = quat[0]
    t.transform.rotation.y = quat[1]
    t.transform.rotation.z = quat[2]
    t.transform.rotation.w = quat[3]
    return t.transform.rotation


def sendtransform():
    global mydynamictf, now, delta_time, robot_x, robot_y, robot_yaw

    #getting delta time
    delta_time = mydynamictf.get_clock().now().nanoseconds / (10 ** 9) - now
    now = mydynamictf.get_clock().now().nanoseconds / (10 ** 9)

    t = TransformStamped()
    stamp = mydynamictf.get_clock().now().to_msg()
    t.header.stamp = stamp
    t.header.frame_id = "world"
    t.child_frame_id = "base_link"
    t.transform.translation.x = robot_x
    t.transform.translation.y = robot_y
    t.transform.translation.z = 0.0
    t.transform.rotation = quaternion_from_euler(0.0, 0.0, robot_yaw)

    br = tf2_ros.transform_broadcaster.TransformBroadcaster(mydynamictf)
    br.sendTransform(t)

def set_robot_velocity(msg):
    global mydynamictf, delta_time, robot_x, robot_y, robot_yaw
    x_vel = msg.linear.x
    yaw_vel = msg.angular.z

    #getting delta position
    delta_yaw = yaw_vel * delta_time
    robot_yaw = robot_yaw + delta_yaw
    robot_x = robot_x + (x_vel * cos(robot_yaw)) * delta_time
    robot_y = robot_y + (x_vel * sin(robot_yaw)) * delta_time
    
def main():
    global mydynamictf, now
    rclpy.init()
    mydynamictf = rclpy.create_node('odom')
    mydynamictf.create_subscription(Twist, '/cmd_vel', set_robot_velocity, 10)    
    mydynamictf.create_timer(1.0 / 100.0, sendtransform)
    now = mydynamictf.get_clock().now().nanoseconds / (10 ** 9)
    try:
        rclpy.spin(mydynamictf)
    except KeyboardInterrupt:
        pass    
    mydynamictf.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()