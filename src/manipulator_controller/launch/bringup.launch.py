import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():   
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory("manipulator_description"), "launch", "gazebo.launch.py")]
        )
    )
    
    controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory("manipulator_controller"), "launch", "controller.launch.py")]
        ),
        launch_arguments={"is_sim": "True"}.items()
    )

    return LaunchDescription([
        gazebo,
        controller
    ])
