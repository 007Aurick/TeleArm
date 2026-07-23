#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class DiffDrivePublisher(Node):
    def __init__(self):
        super().__init__('diff_drive_publisher')
        self.publisher = self.create_publisher(
            TwistStamped,
            '/diff_drive_base_controller/cmd_vel',
            10,
        )
        self.timer = self.create_timer(0.05, self.publish_command)
        self.tick = 0  # your own counter (not a ROS command)

    def publish_command(self):
        self.tick+=1

        if self.tick <=40:
            lin,ang = 0.5,0.0
        elif self.tick <= 50:
            lin,ang = 0.0,0.0
        elif self.tick <= 70:
            lin,ang = 0.0,0.5
        elif self.tick <= 80:
            lin,ang = 0.0,0.0
        else:
            self.tick = 0
            lin,ang = 0.0,0.0
        
        
        command = TwistStamped()
        command.header.stamp = self.get_clock().now().to_msg()
        command.twist.linear.x = lin
        command.twist.angular.z = ang
        self.publisher.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = DiffDrivePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
