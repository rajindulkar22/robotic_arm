import rclpy
from rclpy.node import Node
from manipulator_msgs.srv import EulerToQuaternion, QuaternionToEuler
from tf_transformations import euler_from_quaternion, quaternion_from_euler

class AngleConversion(Node):
    def __init__(self):
        super().__init__("angle_conversion_service_server")
        self.euler_to_quaternion = self.create_service(EulerToQuaternion, "euler_to_quaternion", self.euler_to_quaternion_callback)
        self.quaternion_to_euler = self.create_service(QuaternionToEuler, "quaternion_to_euler", self.quaternion_to_euler_callback)
        self.get_logger().info("Angle conversion service server started")

    def euler_to_quaternion_callback(self, request, response):
        self.get_logger().info("Requested to convert euler to quaternion roll: %f, pitch: %f ,yaw: %f" % (request.roll,request.pitch,request.yaw))
        (response.x,response.y,response.z,response.w) = quaternion_from_euler(request.roll,request.pitch,request.yaw)
        self.get_logger().info("Quaternion: x: %f, y: %f, z: %f, w: %f" % (response.x,response.y,response.z,response.w))
        return response


    def quaternion_to_euler_callback(self, request, response):
        self.get_logger().info("Requested to convert quaternion to euler x: %f, y: %f, z: %f, w: %f" % (request.x,request.y,request.z,request.w))
        (response.roll,response.pitch,response.yaw) = euler_from_quaternion(request.x,request.y,request.z,request.w)
        self.get_logger().info("Euler: roll: %f, pitch: %f, yaw: %f" % (response.roll,response.pitch,response.yaw))
        return response

def main():
    rclpy.init()
    angle_convertor  = AngleConversion()
    rclpy.spin(angle_convertor)
    angle_convertor.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
