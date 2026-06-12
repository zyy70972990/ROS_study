import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_euler
import math 


class TFBroadcaster(Node):
    
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.broadcaster = TransformBroadcaster(self)
        self.timer_ = self.create_timer(0.01,self.publish_tf)
        
    def publish_tf(self):
        
        """
        Broadcast coordinate relationship from camera_link to bottom_link
        """
        
        tranform = TransformStamped()
        tranform.header.frame_id = 'camera_link'
        tranform.child_frame_id = 'bottom_link'
        tranform.header.stamp = self.get_clock().now().to_msg()
        
        tranform.transform.translation.x = 0.2
        tranform.transform.translation.y = 0.3
        tranform.transform.translation.z = 0.5
        
        q = quaternion_from_euler(0,0,0)

        tranform.transform.rotation.x = q[0]
        tranform.transform.rotation.y = q[1]
        tranform.transform.rotation.z = q[2]
        tranform.transform.rotation.w = q[3]
        
        self.broadcaster.sendTransform(tranform)
        self.get_logger().info(f"Broadcast tf: {tranform}")
        

def main():
    
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
    