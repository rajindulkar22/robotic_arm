from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True"
    )

    is_sim = LaunchConfiguration("is_sim")

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("manipulator_description"), 
            "launch", 
            "gazebo.launch.py"
        )
    )

    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("manipulator_controller"), 
            "launch", 
            "controller.launch.py"
        ),
        launch_arguments={"is_sim": is_sim}.items()
    )

    moveit =  IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("manipulator_moveit"), 
            "launch", 
            "moveit.launch.py"
        ),
        launch_arguments={"is_sim": is_sim}.items()
    )

    remote_interface = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("manipulator_remote"), 
            "launch", 
            "remote_interface.launch.py"
        ),
        launch_arguments={"is_sim": is_sim}.items()
    )

    return LaunchDescription([
        is_sim_arg,
        gazebo,
        controller,
        moveit,
        remote_interface
    ])
