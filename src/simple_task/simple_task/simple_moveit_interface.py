#!/usr/bin/env python3
import rclpy
from rclpy.logging import get_logger
import numpy as np
from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState

class SimpleMoveItInterface:
    def __init__(self):
        self.manipulator = MoveItPy(node_name="moveit_py")
        self.arm = self.manipulator.get_planning_component("arm")
        self.gripper = self.manipulator.get_planning_component("gripper")

    def move_to_pose(self):
        arm_state = RobotState(self.manipulator.get_robot_model())
        gripper_state = RobotState(self.manipulator.get_robot_model())

        arm_state.set_joint_group_positions("arm", np.array([1.57, 0.0, 0.0]))
        gripper_state.set_joint_group_positions("gripper", np.array([-0.7, 0.7]))

        self.arm.set_start_state_to_current_state()
        self.gripper.set_start_state_to_current_state()

        self.arm.set_goal_state(robot_state=arm_state)
        self.gripper.set_goal_state(robot_state=gripper_state)

        arm_plan_result = self.arm.plan()
        gripper_plan_result = self.gripper.plan()

        if arm_plan_result and gripper_plan_result:
            self.manipulator.execute(arm_plan_result.trajectory, controllers=[])
            self.manipulator.execute(gripper_plan_result.trajectory, controllers=[])
        else:
            get_logger("rclpy").info("Plan failed")

def main():
    rclpy.init()
    
    # Create the interface object
    interface = SimpleMoveItInterface()
    interface.move_to_pose()
    
    # Explicitly delete the object to trigger destructors before rclpy.shutdown()
    del interface
    
    rclpy.shutdown()

if __name__ == "__main__":
    main()