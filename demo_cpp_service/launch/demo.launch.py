import launch 
import launch_ros

def generate_launch_description():
    
    action_node_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',
        executable ='turtlesim_node',
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
        action_node_turtlesim_node,
        action_node_service_control_node,
        action_node_client_control_node
    ])