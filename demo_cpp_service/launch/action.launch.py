# import os  # 建议添加
# import launch
# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument
# from launch_ros.actions import Node
# from launch_ros.parameter_descriptions import ParameterValue
# from launch.substitutions import LaunchConfiguration
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from ament_index_python.packages import get_package_share_directory # 建议添加

import os
import launch
import launch.launch_description_sources
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, IncludeLaunchDescription, LogInfo,
    ExecuteProcess, GroupAction, TimerAction
)
import launch_ros
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import LaunchConfiguration

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # action1
    multisim_launch_path = os.path.join(
    get_package_share_directory('turtlesim'),
    'launch',
    'multisim.launch.py'
    )
    
    print("hello world")
    action_include_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            multisim_launch_path
        )
    )
    
    
   
    
    action_declare_arg_background_g = launch.actions.DeclareLaunchArgument(
        'launch_arg_bg',default_value='150'
    )
    
    action_declare_startup_rqt = launch.actions.DeclareLaunchArgument(
        'startup_rqt',default_value='False'
    )
    
    action_declare_startup_rqt = DeclareLaunchArgument(
        'startup_rqt', default_value='False'
    )
    
    startup_rqt_cond = LaunchConfiguration('startup_rqt')
    
    action_node_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',
        executable ='turtlesim_node',
        parameters=[{
            'background_g': ParameterValue(
                LaunchConfiguration('launch_arg_bg'),
                value_type=int        # 关键：转为整数
            )
        }],
        output = 'screen'
    )
    
    action_node_service_control_node = launch_ros.actions.Node(
        package='demo_cpp_service',
        executable ='Service_Turtle_Control',
        output = 'log'
    )
    
    action_node_client_control_node = launch_ros.actions.Node(
        package='demo_cpp_service',
        executable ='Client_Turtle_Control',
        output = 'log'
    )
    
    action_log_info = launch.actions.LogInfo(msg=str(multisim_launch_path))
    action_topic_list = launch.actions.ExecuteProcess(
        cmd=['ros2','topic','list']
    )
    
    action_run_rqt = launch.actions.ExecuteProcess(
        condition=IfCondition(startup_rqt_cond),
        cmd=['rqt']
    )
    
    action_group = launch.actions.GroupAction([
        launch.actions.TimerAction(period=2.0,actions=[action_include_launch]),
        launch.actions.TimerAction(period=2.0,actions=[action_topic_list]),
        launch.actions.TimerAction(period=2.0,actions=[action_run_rqt]),
    ])
    
    return launch.LaunchDescription([
        action_log_info,
        action_group
    ])

