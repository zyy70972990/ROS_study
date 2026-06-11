import launch 
import launch_ros
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    
    
    action_declare_arg_background_g = launch.actions.DeclareLaunchArgument(
        'launch_arg_bg',default_value='150'
    )
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
    
    return launch.LaunchDescription([
        action_declare_arg_background_g,
        action_node_turtlesim_node,
        action_node_service_control_node,
        action_node_client_control_node
    ])