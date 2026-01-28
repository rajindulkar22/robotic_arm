import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from rclpy.parameter import Parameter

class SimpleParameterNode(Node):
    def __init__(self):
        super().__init__("simple_parameter_node")
        self.declare_parameter("simple_int_param", 28)
        self.declare_parameter("simple_string_param", "raj")

        self.add_on_set_parameters_callback(self.param_change_callback) # add callback for dynamic parameters

    def param_change_callback(self, params):
        result = SetParametersResult()

        for param in params:
            if param.name == "simple_int_param" and param.type_ == Parameter.Type.INTEGER:
                self.get_logger().info(f"Simple Int Param changed to: {param.value}")
                result.successful = True

            if param.name == "simple_string_param" and param.type_ == Parameter.Type.STRING:
                self.get_logger().info(f"Simple String Param changed to: {param.value}")
                result.successful = True

        return result

def main():
    rclpy.init()
    simple_parameter_node = SimpleParameterNode()
    rclpy.spin(simple_parameter_node)
    simple_parameter_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
