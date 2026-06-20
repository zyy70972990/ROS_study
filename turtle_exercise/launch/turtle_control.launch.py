# import launch
# import launch_ros
# import os
# from ament_index_python.packages import get_package_share_directory
# from launch.substitutions import Command, LaunchConfiguration
# from launch_ros.parameter_descriptions import ParameterValue
# import turtlesim


# def generate_launch_description():
  
    
#     # launch_file_path = get_package_share_directory("turtle_exercise")
#     # turtle_control_node_path = os.path.join(launch_file_path,"turtle_exercise","turtle_control.py")
    
#     turtle_num_param = launch.actions.DeclareLaunchArgument("turtle_num",default_value='1')
    
    
    
#     turtlesim_node = launch_ros.actions.Node(
#         package = "turtlesim",
#         executable = "turtlesim_node",
#     )
    
#     # turtle_control_node = launch_ros.actions.Node(
#     #     package = "turtle_exercise",
#     #     executable = "turtle_control"
#     # )
    
#     turtle_spawn_node = launch_ros.actions.Node(
#         package = "turtle_exercise",
#         executable = "turtle_spawn_service",
#         parameters=[{
#             'Spawn_num': ParameterValue(
#                 LaunchConfiguration('turtle_num'),
#                 value_type=int        # 关键：转为整数
#             )
#         }],
#     )

#     return launch.LaunchDescription([
#         turtle_num_param,
#         turtlesim_node,
#         # turtle_control_node,
#         turtle_spawn_node
#     ])
    
    
# def main():
#     generate_launch_description()


# if __name__ == "__main__":

#     main()
    
   
import launch
import launch_ros
from launch.actions import DeclareLaunchArgument, ExecuteProcess, RegisterEventHandler
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch.event_handlers import OnProcessStart

def generate_launch_description():
    # 1. 声明参数
    order_num_param = DeclareLaunchArgument(
        "order",
        default_value='6',
        description="Order value for the move action"
    )

    # 2. 定义三个核心进程（注意：这里只定义，不直接放入 LaunchDescription）
    turtlesim_node = Node(
        package="turtlesim",
        executable="turtlesim_node",
    )

    # 你的 Action 服务端节点
    action_server_node = Node(
        package="turtle_exercise",
        executable="turtle_target_control",
    )

    # Action 客户端命令
    goal_json = Command([
        "echo '{\"order\": ", LaunchConfiguration('order'), "}'"
    ])
    goal_client = ExecuteProcess(
        cmd=[
            'ros2', 'action', 'send_goal', '--feedback',
            '/turtle_move',
            'status_interfaces/action/Move',
            goal_json
        ],
        output='screen'
    )

    # 3. 构建启动顺序（事件驱动）
    return launch.LaunchDescription([
        order_num_param,
        
        # 第一步：启动 turtlesim
        turtlesim_node,
        
        # 第二步：当 turtlesim 启动成功后，再启动 Action Server
        RegisterEventHandler(
            OnProcessStart(
                target_action=turtlesim_node,
                on_start=[action_server_node]
            )
        ),
        
        # 第三步：当 Action Server 启动成功后，再启动客户端
        RegisterEventHandler(
            OnProcessStart(
                target_action=action_server_node,
                on_start=[goal_client]
            )
        )
    ])
    
