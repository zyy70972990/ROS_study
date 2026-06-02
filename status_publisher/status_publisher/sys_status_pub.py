import rclpy
from status_interfaces.msg import Systemstatus
from rclpy.node import Node
import psutil
import platform

class SystStatusPub(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.statu_publisher_ = self.create_publisher(
            Systemstatus,'sys_status',10
        )
        self.timers_ = self.create_timer(1.0,self.timer_callback)

    def timer_callback(self):

        # builtin_interfaces/Time stamp
        # string host_name
        # float32 cpu_percentage
        # float32 memory_percentage
        # float32 memory_available
        # float64 net_send
        # float64 net_recv

        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        net_io_counters = psutil.net_io_counters()
        msg = Systemstatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.host_name = platform.node()
        msg.cpu_percentage = cpu_percent
        msg.memory_percentage = memory_info.percent
        msg.memory_total = float(memory_info.total)
        msg.memory_available = float(memory_info.available)
        msg.net_send = float(net_io_counters.bytes_sent)
        msg.net_recv = float(net_io_counters.bytes_recv)

        self.get_logger().info(f'publish:{str(msg)}')
        self.statu_publisher_.publish(msg)

def main():

    rclpy.init()
    node = SystStatusPub('sys_state_pub')
    rclpy.spin(node)
    rclpy.shutdown()
