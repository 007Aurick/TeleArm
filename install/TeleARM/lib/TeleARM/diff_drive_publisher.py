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

    def publish_command(self):
        command = TwistStamped()
        command.header.stamp = self.get_clock().now().to_msg()
        command.twist.linear.x = 0.4
        command.twist.angular.z = 0.4
        self.publisher.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = DiffDrivePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
