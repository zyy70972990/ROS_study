#!/usr/bin/env python3
import face_recognition
import cv2
import os
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory

def main():
    # 获取图片路径（使用绝对路径）
    # 方法1：直接指定路径
    image_path = '/home/y2x/project/ros_ws/src/demo_python_service/resource/test.jpeg'
    
    # 方法2：使用 ROS 包路径（推荐）
    # package_dir = get_package_share_directory('demo_python_service')
    # image_path = os.path.join(package_dir, 'resource', 'test.jpeg')
    
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"错误：图片文件不存在 {image_path}")
        print("请确保图片存在，或修改 image_path 变量")
        return
    
    try:
        # 加载图片
        print(f"正在加载图片: {image_path}")
        image = face_recognition.load_image_file(image_path)
        print(f"图片加载成功，尺寸: {image.shape}")
        
        # 方法1：检测人脸位置（返回边界框坐标）
        print("正在检测人脸...")
        face_locations = face_recognition.face_locations(image, model='hog')
        # face_locations 返回 [(top, right, bottom, left), ...]
        
        # 方法2：获取人脸编码（128维特征向量）
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        # 方法3：检测人脸关键点（眼睛、鼻子等）
        face_landmarks = face_recognition.face_landmarks(image, face_locations)
        
        print(f"检测到 {len(face_locations)} 张人脸")
        
        # 将 RGB 转换为 BGR（OpenCV 使用 BGR）
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 在图片上绘制人脸框和关键点
        for i, (top, right, bottom, left) in enumerate(face_locations):
            print(f"人脸 {i+1}: 上={top}, 右={right}, 下={bottom}, 左={left}")
            
            # 绘制人脸框
            cv2.rectangle(image_bgr, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # 绘制人脸关键点（如果有）
            if face_landmarks and i < len(face_landmarks):
                landmarks = face_landmarks[i]
                for feature_name, points in landmarks.items():
                    for point in points:
                        cv2.circle(image_bgr, point, 1, (0, 0, 255), -1)
            
            # 在框上方添加标签
            cv2.putText(image_bgr, f"Face {i+1}", (left, top-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # 显示图片
        cv2.imshow('Face Detection', image_bgr)
        print("按任意键关闭窗口...")
        cv2.waitKey()
        cv2.destroyAllWindows()
        
        # 可选：保存结果图片  
        output_path = '/home/y2x/project/ros_ws/detection_result.jpg'
        cv2.imwrite(output_path, image_bgr)
        print(f"结果已保存到: {output_path}")
        
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == '__main__':
    main()