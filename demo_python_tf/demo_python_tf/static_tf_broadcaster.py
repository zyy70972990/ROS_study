import rclpy
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_euler
import math 

class StaticTFBroadcaster(Node):
    
    def __init__(self):
        super().__init__('static_tf_broadcaster')
        self.static_broadcaster = StaticTransformBroadcaster(self)
        self.publish_static_tf() 
    
    def publish_static_tf(self):
        
        """
        Broadcast coordinate relationship from base_link to camera_link
        """
        
        tranform = TransformStamped()
        tranform.header.frame_id = 'base_link'
        tranform.child_frame_id = 'camera_link'
        tranform.header.stamp = self.get_clock().now().to_msg()
        
        tranform.transform.translation.x = 0.5
        tranform.transform.translation.y = 0.3
        tranform.transform.translation.z = 0.6
        
        q = quaternion_from_euler(math.radians(180),0,0)

        tranform.transform.rotation.x = q[0]
        tranform.transform.rotation.y = q[1]
        tranform.transform.rotation.z = q[2]
        tranform.transform.rotation.w = q[3]
        
        self.static_broadcaster.sendTransform(tranform)
        self.get_logger().info(f"Broadcast tf: {tranform}")
        

def main():
    
    rclpy.init()
    node = StaticTFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
    