import rclpy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

def joy_callback(msg):
    global teleopPub
    twist_msg = Twist()
    
    if msg.axes[5] == 1.0: 
        twist_msg.linear.x = msg.axes[1]
        twist_msg.angular.z = msg.axes[3]
        teleopPub.publish(twist_msg)
    else:
        print('deadman active')

def main():
    global teleopPub
    rclpy.init()
    node = rclpy.create_node('teleop')
    subscription = node.create_subscription(Joy, '/joy', lambda msg: joy_callback(msg), 10)
    teleopPub = node.create_publisher(Twist, '/cmd_vel', 10)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('Exited')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()