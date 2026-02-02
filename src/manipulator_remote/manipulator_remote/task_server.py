#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from manipulator_msgs.action import ManipulatorTask
import time
from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState
import numpy as np


class TaskServer(Node):
    def __init__(self):
        super().__init__("task_server")
        self.get_logger().info("Starting the Server")
        self.action_server = ActionServer(
            self, ManipulatorTask, "task_server", self.goalCallback
        )
        self.manipulator = MoveItPy(node_name="moveit_py")
        self.manipulator_arm = self.manipulator.get_planning_component("arm") #arm planning component   
        self.manipulator_gripper = self.manipulator.get_planning_component("gripper") #gripper planning component


    def goalCallback(self, goal_handle):
        self.get_logger().info(
            "Received goal request with task_number %d" % goal_handle.request.task_number
        )

        arm_state = RobotState(self.manipulator.get_robot_model()) #current state of the arm
        gripper_state = RobotState(self.manipulator.get_robot_model()) #current state of the gripper

        arm_joint_goal = []
        gripper_joint_goal = []
        #these are the target position of the arm and gripper
        if goal_handle.request.task_number == 0: # if task number is 0
            arm_joint_goal = np.array([0.0, 0.0, 0.0])
            gripper_joint_goal = np.array([-0.7, 0.7])

        elif goal_handle.request.task_number == 1: # if task number is 1
            arm_joint_goal = np.array([-1.14,-0.6,-0.07]) #values are in radians of the joint
            gripper_joint_goal = np.array([-0.0, 0.0])

        elif goal_handle.request.task_number == 2: # if task number is 2
            arm_joint_goal = np.array([-1.57, 0.0, -0.9]) #values are in radians of the joint
            gripper_joint_goal = np.array([-0.0, 0.0])

        else:
            self.get_logger().info("Invalid task number")
            return 


        arm_state.set_joint_group_positions("arm", arm_joint_goal)
        gripper_state.set_joint_group_positions("gripper", gripper_joint_goal)

        self.manipulator_arm.set_start_state_to_current_state()
        self.manipulator_gripper.set_start_state_to_current_state()

        self.manipulator_arm.set_goal_state(robot_state=arm_state)
        self.manipulator_gripper.set_goal_state(robot_state=gripper_state)

#plan the trajectory
        arm_plan_result = self.manipulator_arm.plan()
        gripper_plan_result = self.manipulator_gripper.plan()


        if arm_plan_result and gripper_plan_result:
            self.manipulator.execute(arm_plan_result.trajectory, controllers=[])
            self.manipulator.execute(gripper_plan_result.trajectory, controllers=[])


        else:
            self.get_logger().info("one or more plan failed")

        goal_handle.succeed()
        result = ManipulatorTask.Result()
        result.success=True
        return result



def main(args=None):
    rclpy.init(args=args)
    task_server = TaskServer()
    rclpy.spin(task_server)


if __name__ == "__main__":
    main()