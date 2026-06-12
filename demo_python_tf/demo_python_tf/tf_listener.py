import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener,Buffer,TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf_transformations import euler_from_quaternion
import math 


class TFBroadcaster(Node):
    
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.buffer_ = Buffer()
        self.listener_ = TransformListener(self.buffer_,self)
        self.timer_ = self.create_timer(1.0,self.get_transform)
        
    
    def get_transform(self):
        
        """
        get current coordinate relationship
        """
        
        try:
            result = self.buffer_.lookup_transform('bottom_link','camera_link',rclpy.time.Time(seconds=0),rclpy.time.Duration(seconds=1))
            transform = result.transform
            self.get_logger().info(f"translate : {transform.translation}")
            self.get_logger().info(f"translate : {transform.rotation}")
            
            rotation_euler = euler_from_quaternion([
                transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w]
            )
            self.get_logger().info(f"rotation RPY : {rotation_euler}")
            
           
        except Exception as e:
            self.get_logger().warn(f"fail to get coordiate transformation with error :{str(e)}")
            
    
        

def main():
    
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
    