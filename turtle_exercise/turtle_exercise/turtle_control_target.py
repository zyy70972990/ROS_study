# import rclpy
# import turtlesim 
# from rclpy.node import Node
# from geometry_msgs.msg import Twist
# import math
# import time
# from rclpy.action import ActionServer
# from status_interfaces.action import Move
# from turtlesim.srv import TeleportAbsolute


# class Turtle_Control_Target(Node):
    
#     def __init__(self,NodeName):
#         super().__init__(NodeName)
#         self.ActionServer_ = ActionServer(self,Move,"/turtle_move",self.execute_callback)
#         self.client_ =  self.create_client(TeleportAbsolute,'/turtle1/teleport_absolute')
#         # while self.client_.wait_for_service(timeout_sec=1.0) is False:
#         #     self.get_logger().info('Service is not avaiable, waiting again...')
#         self.get_logger().info('Teleport client created, will check availability when executing goal.')
#         self.req = TeleportAbsolute.Request()

#     def calculate_polygon_vertices(self,base_length,num_sides,fix_x,fix_y):
        
#         angle_increment = 360/num_sides
#         angle_radians = math.radians(angle_increment/2)
#         sin_hale_theta = math.radians(angle_radians)
#         radius = base_length/(2*sin_hale_theta)
#         self.vertices = []
        
#         for i in range(num_sides-1):
#             angle_deg = (i+1)*angle_increment
#             angle_rad = math.radians(angle_deg)
#             x = fix_x-radius+radius*math.cos(angle_rad)
#             y = fix_y+radius*math.sin(angle_rad)
#             self.vertices.append((x,y))
#         self.vertices.append(fix_x,fix_y)
        
#     def send_request(self,x,y,theta):
        
#         self.req.x = x
#         self.req.y = y 
#         self.req.theta = theta
        
#         future = self.client_.call_async(self.req)
#         future.add_done_callback(self.callback)
        
#     def callback(self, future):
#         try:
#             response = future.result()
#             self.get_logger().info('Teleport successful')
#         except Exception as e:
#             self.get_logger().info(f"Service call failed {e}")
        
#     def execute_callback(self,goal_handle):
        
#         if not self.client_.wait_for_service(timeout_sec=5.0):
#             self.get_logger().error('Teleport service still not available')
#             goal_handle.abort()
#         return Move.Result(success=False)
    
#         self.get_logger().info('Executing goal...')
#         feedback_msg = Move.Feedback()
#         feedback_msg.partial_sequence = []
#         self.calculate_polygon_vertices(1.5,goal_handle.request.order,5.5,5.5)
        
# def main():
    
#     rclpy.init()
#     node = Turtle_Control_Target("TargetContronNode")
#     rclpy.spin(node)
#     rclpy.shutdown()


import rclpy
from rclpy.node import Node
import math
import time
from rclpy.action import ActionServer
from status_interfaces.action import Move
from turtlesim.srv import TeleportAbsolute
from rclpy.executors import MultiThreadedExecutor

class Turtle_Control_Target(Node):
    def __init__(self, NodeName):
        super().__init__(NodeName)
        self.ActionServer_ = ActionServer(
            self, Move, "/turtle_move",
            self.execute_callback
        )
        self.client_ = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.get_logger().info('Teleport client created.')
        
        if not self.client_.wait_for_service(timeout_sec=3.0):
            self.get_logger().error('Teleport service not available')
        

    def calculate_polygon_vertices(self, base_length, num_sides, fix_x, fix_y):
        angle_increment = 360.0 / num_sides
        half_angle_deg = angle_increment / 2.0
        half_angle_rad = math.radians(half_angle_deg)
        radius = base_length / (2 * math.sin(half_angle_rad))
        vertices = []
        for i in range(num_sides):
            i+=1
            angle_deg = i * angle_increment
            angle_rad = math.radians(angle_deg)
            x = fix_x - radius + radius * math.cos(angle_rad)
            y = fix_y + radius * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices

    def send_teleport_sync(self, x, y, theta=0.0, timeout=1.0):
        """同步传送乌龟，通过轮询等待 future 完成，并设置超时"""
        req = TeleportAbsolute.Request()
        req.x = x
        req.y = y
        req.theta = theta
        future = self.client_.call_async(req)
        # 轮询等待，不调用 spin_until_future_complete
        start = time.time()
        while not future.done():
            if time.time() - start > timeout:
                raise TimeoutError(f'Teleport service call timed out after {timeout}s')
            time.sleep(0.01)  # 避免忙等
        # 获取结果（可能抛出异常）
        return future.result()

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        order = goal_handle.request.order

        if order < 3:
            self.get_logger().error('Order must be at least 3')
            goal_handle.abort()
            return Move.Result(target_pos=[])

        # if not self.client_.wait_for_service(timeout_sec=3.0):
        #     self.get_logger().error('Teleport service not available')
        #     goal_handle.abort()
        #     return Move.Result(target_pos=[])

        vertices = self.calculate_polygon_vertices(1.5, order, 5.5, 5.5)
        self.get_logger().info(f'Calculated {len(vertices)} vertices')

        feedback_msg = Move.Feedback()
        feedback_msg.cur_pos = []
        for i, (x, y) in enumerate(vertices):
            self.get_logger().info(f'Moving to vertex {i+1}: ({x:.3f}, {y:.3f})')
            try:
                self.send_teleport_sync(x, y, 0.0)
            except Exception as e:
                self.get_logger().error(f'Teleport failed: {e}')
                goal_handle.abort()
                return Move.Result(target_pos=[])

            feedback_msg.cur_pos = [x, y]
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(0.2)  # 短暂延时

        goal_handle.succeed()
        result = Move.Result()
        result.target_pos = [coord for v in vertices for coord in v]
        self.get_logger().info('Goal completed successfully!')
        return result

def main():
    rclpy.init()
    node = Turtle_Control_Target("TargetContronNode")
    # rclpy.spin(node)
    # node.shutdown()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()