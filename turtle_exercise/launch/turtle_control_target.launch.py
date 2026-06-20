import launch
import launch_ros
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
    # 声明 order 参数，默认值为 6
    order_num_param = DeclareLaunchArgument(
        "order",
        default_value='6',
        description="Order value for the move action"
    )

    # 启动 turtlesim 节点
    turtlesim_node = Node(
        package="turtlesim",
        executable="turtlesim_node",
    )

    
    goal_json = Command([
    "echo '{\"order\": ", LaunchConfiguration('order'), "}'"
    ])

 
    # 执行 ros2 action send_goal 命令
    turtle_action = ExecuteProcess(
        cmd=[
            'ros2', 'action', 'send_goal', '--feedback',
            '/turtle_move',
            'status_interfaces/action/Move',
            goal_json
        ],
        output='screen'  # 将命令输出打印到终端
    )


    action_server_node = Node(
        package="turtle_exercise",
        executable="turtle_target_control",  # 确保与 setup.py 中 entry_points 的名称一致
        output='screen',
    )
    return launch.LaunchDescription([
        order_num_param,
        turtlesim_node,
        action_server_node,
        turtle_action,
        
    ])