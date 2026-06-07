import rclpy
from rclpy.node import Node
from facial_recognition.srv import FaceDetector
import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory
import os
from cv_bridge import CvBridge
import time 
from rcl_interfaces.msg import SetParametersResult

class FaceDetectNode(Node):
    def __init__(self):
        super().__init__('face_detect_node')
        self.service_ = self.create_service(FaceDetector,'face_detect',
                                            self.detect_face_callback)
        self.bridge = CvBridge()
       
        self.default_image_path = os.path.join(get_package_share_directory('demo_python_service'),'resource/test.jpeg')
        self.get_logger().info(f"Server init finished")
        
        self.declare_parameter('number_of_times_to_upsample',1)
        self.declare_parameter('model','hog')
        
        self.model = self.get_parameter('model').value
        self.number_of_times_to_upsample = self.get_parameter('number_of_times_to_upsample').value
        
        self.add_on_set_parameters_callback(self.parameter_callback)
        
    
    # def parameter_callback(self,parameters):
        
    #     for parameter in parameters:
    #         self.get_logger().info(f"{parameter.name}->{parameter.value}")
    #         if parameter.name == 'number_of_times_to_upsample':
    #             self.number_of_times_to_upsample = parameter.value
    #         if parameter.name == 'model':
    #             self.model = parameter.value
                
    #     return SetParametersResult(Successful=True)
    
    
    def parameter_callback(self, params):
        for param in params:
            if param.name == 'model' and param.value in ['hog', 'cnn']:
                self.model = param.value
                self.get_logger().info(f'Model changed to {self.model}')
        return SetParametersResult(Successful=True)
            
            
        
    def detect_face_callback(self,request,response):
        
        self.get_logger().info(f"Server get response")
        if request.image.data:
            cv_image = self.bridge.imgmsg_to_cv2(request.image)
        else:
            cv_image = cv2.imread(self.default_image_path)
        
        start_time = time.time()
        self.get_logger().info(f"Finished loading image, start to recognize")
        face_locations = face_recognition.face_locations(cv_image,number_of_times_to_upsample=self.number_of_times_to_upsample,model=self.model)
        response.use_time = time.time()-start_time
        response.number = len(face_locations)
        
        for i, (top, right, bottom, left) in enumerate(face_locations):
            print(f"人脸 {i+1}: 上={top}, 右={right}, 下={bottom}, 左={left}")
            
            response.top.append(top)
            response.right.append(right)
            response.bottom.append(bottom)
            response.left.append(left)
            
            
          

        
        self.get_logger().info(f"Server send back to client")
        return response

        
    
def main():
    rclpy.init()
    node = FaceDetectNode()
    rclpy.spin(node)
    rclpy.shutdown()