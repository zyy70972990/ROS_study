#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include "iostream"
#include <chrono>

using namespace std::chrono_literals;


class TurtleControlNode: public rclcpp::Node
{

private:
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscriber_;

    float x_;
    float y_;

    
    float x_target;
    float y_target;
    float pre_angle;
    float pre_vel;

public:

    void get_pose_callback(const turtlesim::msg::Pose::SharedPtr pose){

        auto msg = geometry_msgs::msg::Twist();

        x_ = pose->x;
        y_ = pose->y;

        RCLCPP_INFO(get_logger(),"current pos : x = %0.2f, y = %0.2f\n",x_,y_);

        float x_diff = x_target-x_;
        float y_diff = y_target-y_;

        float distance = sqrt(x_diff*x_diff+y_diff*y_diff);
        float cur_angle = std::atan2(y_diff,x_diff)-pose->theta;

        
        msg.angular.z = pre_angle;
      

        RCLCPP_INFO(get_logger(),"current angle : %0.2f\n",cur_angle);
   
        if(distance>0.1){
            if(cur_angle>0.2){
                msg.angular.z = cur_angle;
            }
            else{
                msg.linear.x = distance;
            }
        }


        

        publisher_->publish(msg);

        pre_angle = msg.angular.z;
        pre_vel = msg.linear.x;
  
    }
    explicit TurtleControlNode(const std::string & node_name):Node(node_name)
    {
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel",10);
        subscriber_ = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose",10,std::bind(&TurtleControlNode::get_pose_callback,this,std::placeholders::_1));
        timer_ = this->create_wall_timer(100ms,std::bind(&TurtleControlNode::timer_callback,this));
        // timer_ = this->create_wall_timer(1000ms,[this](){this->timer_callback();}

        x_target = 10;
        y_target = 10;
        pre_angle = 0;
        pre_vel = 1;
    }
        
        
    
    

    void timer_callback(){

        

        
    }


    
};

int main(int argc, char const *argv[])
{
    rclcpp::init(argc,argv);

    auto TurtleControlNode_ = std::make_shared<TurtleControlNode>("TurtleControlNode");

    rclcpp::spin(TurtleControlNode_);

    rclcpp::shutdown();

    return 0;

    
}
