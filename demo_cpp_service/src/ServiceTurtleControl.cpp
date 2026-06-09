#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "turtlesim/msg/pose.hpp"
#include "iostream"
#include <chrono>
#include "demo_cpp_service/srv/turtle_control.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"


using ServiceTurtleControl = demo_cpp_service::srv::TurtleControl;
using SetParametersResult = rcl_interfaces::msg::SetParametersResult;

using namespace std::chrono_literals;


class TurtleControlNode: public rclcpp::Node
{

private:

    OnSetParametersCallbackHandle::SharedPtr parameter_callback_handle_;
    rclcpp::Service<ServiceTurtleControl>::SharedPtr ServiceTurtleController_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscriber_;

    float x_;
    float y_;

    
    float x_target{10};
    float y_target{10};
    float k_{1.0};
    float max_velocity_{3.0};

public:

    explicit TurtleControlNode(const std::string & node_name):Node(node_name)
        {
            
            parameter_callback_handle_ = this->add_on_set_parameters_callback([&](const std::vector<rclcpp::Parameter> &parameters){
                rcl_interfaces::msg::SetParametersResult result;
                result.successful = true;
                for(const auto &parameter : parameters){
                   
                    RCLCPP_INFO(this->get_logger(),"Update the parameter %s=%f",parameter.get_name().c_str(),parameter.as_double());
                    if(parameter.get_name()=="k"){
                        k_ = parameter.as_double();
                    }
                    if(parameter.get_name()=="max_velocity"){
                        max_velocity_ = parameter.as_double();
                    }
                    
                }
                return result;
            });
            this->declare_parameter("k",1.0);
            this->declare_parameter("max_velocity",1.0);
            this->get_parameter("k",k_);
            this->get_parameter("max_velocity",max_velocity_);

            RCLCPP_INFO(this->get_logger(), "Parameters declared: k=%f, max_velocity=%f", k_, max_velocity_);

            ServiceTurtleController_ = this->create_service<ServiceTurtleControl>("Controller",[&](const ServiceTurtleControl::Request::SharedPtr request,ServiceTurtleControl::Response::SharedPtr response){
                if((request->target_x&&request->target_x<12)&&(request->target_y&&request->target_y<12))
                {
                    this->x_target = request->target_x;
                    this->y_target = request->target_y;

                    response->result = ServiceTurtleControl::Response::SUCCESS;
                }else{
                    response->result = ServiceTurtleControl::Response::FAIL;
                }


                
                
            });
            publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel",10);
            subscriber_ = this->create_subscription<turtlesim::msg::Pose>("/turtle1/pose",10,std::bind(&TurtleControlNode::get_pose_callback,this,std::placeholders::_1));
            // timer_ = this->create_wall_timer(100ms,std::bind(&TurtleControlNode::timer_callback,this));
            // timer_ = this->create_wall_timer(1000ms,[this](){this->timer_callback();}

        
        
        }

    void get_pose_callback(const turtlesim::msg::Pose::SharedPtr pose){

        auto msg = geometry_msgs::msg::Twist();

        x_ = pose->x;
        y_ = pose->y;

        RCLCPP_INFO(get_logger(),"current pos : x = %0.2f, y = %0.2f\n",x_,y_);

        float x_diff = x_target-x_;
        float y_diff = y_target-y_;

        float distance = sqrt(x_diff*x_diff+y_diff*y_diff);
        float cur_angle = std::atan2(y_diff,x_diff)-pose->theta;

        
        // msg.angular.z = pre_angle;
      

        RCLCPP_INFO(get_logger(),"distance :%0.2f, pose : %0.2f, current angle : %0.2f, \n",distance,pose->theta,cur_angle);
   
        if(distance>0.1){
            if(cur_angle>0.2){
                msg.angular.z = cur_angle;
            }
            else{
                msg.linear.x = distance;
            }
        }


        

        publisher_->publish(msg);

        // pre_angle = msg.angular.z;
        // pre_vel = msg.linear.x;
  
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
