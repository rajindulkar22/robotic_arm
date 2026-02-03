from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder
from launch.conditions import IfCondition, UnlessCondition
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node




def generate_launch_description():

    is_sim_arg = DeclareLaunchArgument( "is_sim",
    default_value="True")

    use_python_arg = DeclareLaunchArgument("use_python", default_value="False")

    is_sim = LaunchConfiguration("is_sim")
    use_python = LaunchConfiguration("use_python")

    

    moveit_config = (
        MoveItConfigsBuilder("manipulator", package_name="manipulator_moveit")
        .robot_description(file_path=os.path.join(get_package_share_directory("manipulator_description"), "urdf", "manipulator.urdf.xacro"))
        .robot_description_semantic(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "manipulator.srdf"))
        .trajectory_execution(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "moveit_controllers.yaml"))
        .robot_description_kinematics(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "kinematics.yaml"))
        .joint_limits(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "joint_limits.yaml"))
        .pilz_cartesian_limits(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "pilz_cartesian_limits.yaml"))
        .moveit_cpp(file_path=os.path.join(get_package_share_directory("manipulator_moveit"), "config", "planning_python_api.yaml"))
        .to_moveit_configs()
    )

    task_server_node_py = Node(
        package="manipulator_remote",
        executable="task_server.py",
        condition=IfCondition(use_python),
        parameters=[moveit_config.to_dict(),
        {"use_sim_time":is_sim}]
    )

    alexa_interface_node_py = Node(
        package="manipulator_remote",
        executable="alexa_interface.py",
        parameters=[{"use_sim_time":is_sim}]
    )

    return LaunchDescription([
        use_python_arg,
        is_sim_arg,
        task_server_node_py,
        alexa_interface_node_py
    ])
