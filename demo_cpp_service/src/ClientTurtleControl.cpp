#include "rclcpp/rclcpp.hpp"
#include "demo_cpp_service/srv/turtle_control.hpp"
#include <chrono>
#include <ctime>

using ServiceTurtleControl = demo_cpp_service::srv::TurtleControl;
using namespace std::chrono_literals;


class ClientControlNode: public rclcpp::Node
{

private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Client<ServiceTurtleControl>::SharedPtr ClientTurtleControl_;


public:

    
    
    ClientControlNode(const std::string & node_name):Node(node_name)
    {
        ClientTurtleControl_ = this->create_client<ServiceTurtleControl>("Controller");
        timer_ = this->create_wall_timer(5s,[&](){
            while(!this->ClientTurtleControl_->wait_for_service(1s)){
                if(!rclcpp::ok()){
                    RCLCPP_ERROR(this->get_logger(),"Fail to wait for server online, rclcpp stop");
                    return;
                }
                RCLCPP_INFO(this->get_logger(),"Waiting for server online.....");
                srand(time(NULL));
            }

            auto request = std::make_shared<ServiceTurtleControl::Request>();
            
            request->target_x = rand() % 12;
            request->target_y = rand() % 12;

            RCLCPP_INFO(this->get_logger(),"Target pos %f,%f",request->target_x,request->target_x);

            ClientTurtleControl_->async_send_request(request,[&]
                (rclcpp::Client<ServiceTurtleControl>::SharedFuture result_future){
                auto response = result_future.get();
                if(response->result == ServiceTurtleControl::Response::SUCCESS){
                    RCLCPP_ERROR(this->get_logger(),"Request Success");
                }
                if(response->result == ServiceTurtleControl::Response::FAIL){
                    RCLCPP_ERROR(this->get_logger(),"Request Fail");
                }   
            });
        });
    }
        
        
    
    



    
};

int main(int argc, char const *argv[])
{
    rclcpp::init(argc,argv);

    auto ClientControlNode_ = std::make_shared<ClientControlNode>("ClientControlNode");

    rclcpp::spin(ClientControlNode_);

    rclcpp::shutdown();

    return 0;

    
}
