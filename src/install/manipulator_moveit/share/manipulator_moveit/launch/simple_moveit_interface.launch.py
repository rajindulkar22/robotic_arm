from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node




def generate_launch_description():

    

    moveit_config = (
        MoveItConfigsBuilder("manipulator", package_name="manipulator_moveit")
        .robot_description(file_path=os.path.join(get_package_share_directory("manipulator_description"), "urdf", "manipulator.urdf.xacro"))
        .robot_description_semantic(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "manipulator.srdf"))
        .trajectory_execution(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "moveit_controllers.yaml"))
        .robot_description_kinematics(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "kinematics.yaml"))
        .joint_limits(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "joint_limits.yaml"))
        .pilz_cartesian_limits(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "pilz_cartesian_limits.yaml"))
        .to_moveit_configs()
        .moveit_cpp(file_path="config/planning_python_api.yaml")
    )

    moveit_interface_node = Node(
        package="manipulator_moveit",
        executable="moveit_interface",
        name="move_robot",
        output="screen",
        parameters=[moveit_config.to_dict(),
        {"use_sim_time":True}]
    )

    return LaunchDescription([
        moveit_interface_node
    ])
