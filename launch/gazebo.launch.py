from launch import LaunchDescription
from launch.actions import (
    ExecuteProcess,
    IncludeLaunchDescription,
    RegisterEventHandler,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py',
            ])
        ]),
        launch_arguments={
            'use_sim_time': 'true',
        }.items(),
    )

    robot_description = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([
            FindPackageShare('wheeled_robot'),
            'urdf',
            'cybertruck.urdf.xacro',
        ]),
    ])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': robot_description},
            {'use_sim_time': True},
        ],
        output='screen',
    )

    robot_spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'robot',
            '-z', '0.5',
            '-timeout', '180.0',
        ],
        output='screen',
    )

    load_joint_state_broadcaster = ExecuteProcess(
        cmd=[
            'ros2', 'control', 'load_controller',
            '--set-state', 'active',
            'joint_state_broadcaster',
        ],
        output='screen',
    )

    load_diff_drive_base_controller = ExecuteProcess(
        cmd=[
            'ros2', 'control', 'load_controller',
            '--set-state', 'active',
            'diff_drive_base_controller',
        ],
        output='screen',
    )

    diff_drive_publisher_node = Node(
        package='wheeled_robot',
        executable='diff_drive_publisher.py',
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    load_broadcaster_after_spawn = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=robot_spawn_node,
            on_exit=[load_joint_state_broadcaster],
        )
    )

    load_diff_drive_after_broadcaster = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=load_joint_state_broadcaster,
            on_exit=[load_diff_drive_base_controller],
        )
    )

    start_publisher_after_controller = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=load_diff_drive_base_controller,
            on_exit=[diff_drive_publisher_node],
        )
    )

    return LaunchDescription([
        gazebo_launch,
        robot_state_publisher_node,
        robot_spawn_node,
        load_broadcaster_after_spawn,
        load_diff_drive_after_broadcaster,
        start_publisher_after_controller,
    ])