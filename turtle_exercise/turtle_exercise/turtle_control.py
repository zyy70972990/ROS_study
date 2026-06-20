import rclpy
import turtlesim 
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleControl(Node):
    
    def __init__(self,node_name):
        super().__init__(node_name)
        self.turtle_name_ = self.declare_parameter("turtle_name","turtle1").get_parameter_value().string_value
       
        self.vel_publisher_ = self.create_publisher(Twist,f"{self.turtle_name_}/cmd_vel",10)
        self.timer_ = self.create_timer(0.01,self.TimerCallback)
        self.counter = 0
        
        
    def TimerCallback(self):
        
        vel = Twist()
        vel.angular.z = 2.0
        vel.linear.x = 0.002*self.counter
       
        self.counter+=1
        self.get_logger().info(f"published:{str(vel)}",)
        self.vel_publisher_.publish(vel)



def main():
    
    rclpy.init()
    node = TurtleControl("turtle_spiral_move_control")
    rclpy.spin(node)
    rclpy.shutdown()
    