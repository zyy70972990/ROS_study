import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
import string
import random
import time 
from random import random
from rcl_interfaces.msg import SetParametersResult

class TurtleSpawnService(Node):
    
    def __init__(self,node_name):
        super().__init__(node_name)
        
        self.client_ = self.create_client(Spawn,"/spawn")
        
        while self.client_.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info('Waiting for parameter server start')
        
        
        # self.server_ = self.create_service()
       
            
        self.spwanID = 1
        
        
        self.declare_parameter("Spawn_num",1)
        self.spawn_num = self.get_parameter("Spawn_num").value
        
        self.add_on_set_parameters_callback(self.parameter_callback)
        
        self.timer_ = self.create_timer(0.1,self.SpawnRequest)
        
        
    def SpawnRequest(self):
    
        
            
        while(self.spwanID<=self.spawn_num):
            spawn = Spawn.Request()
            spawn.x = random()*10
            self.get_logger().info(f"random : {spawn.x}")
            spawn.y = random()*10
            spawn.name = f"turtle_{self.spwanID}"
            future = self.client_.call_async(spawn)
            # rclpy.spin_until_future_complete(self,future)
            future.add_done_callback(self.spawn_response_callback)
                # 为避免同时生成多个导致服务端过载，添加小延时
            self.spwanID+=1

        # response = future.result()
                   
    
    def parameter_callback(self,params):
        
        for param in params:
            if param.name == 'Spawn_num':
                self.spawn_num = param.value
                self.get_logger().info(f'Set spawn num :{self.spawn_num}')
  
        return SetParametersResult(successful=True)
    
    def spawn_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Spawned turtle: {response.name}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
    
        
            
def main():
    
    rclpy.init()
    Node = TurtleSpawnService("TurtleSpawnClientNode")

    rclpy.spin(Node)
    rclpy.shutdown()


