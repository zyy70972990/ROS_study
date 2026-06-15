import launch
import launch_ros
import os
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    
    urdf_pacakge_path = get_package_share_directory('demo_robot_description')
    default_urdf_path = os.path.join(urdf_pacakge_path,'urdf','demo_robot.xacro')
    default_rviz_config_path = os.path.join(urdf_pacakge_path,'config','display_robot_model.rviz')
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model_path',default_value=str(default_urdf_path),description='the path of loaded urdf file'
    )
    
    # substitutions_command_result = Command(['cat ',LaunchConfiguration('model_path')])
    substitutions_command_result = Command(['xacro ',LaunchConfiguration('model_path')])
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(substitutions_command_result,value_type=str)
    
    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters= [{'robot_description':robot_description_value}]
    )
    
    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )
    
    action_rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d',default_rviz_config_path]
    )
    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node
    ])

