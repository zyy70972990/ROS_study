#include "rclcpp/rclcpp.hpp"
#include "demo_cpp_service/srv/turtle_control.hpp"
#include <chrono>
#include <ctime>
#include "rcl_interfaces/msg/parameter.hpp"
#include "rcl_interfaces/msg/parameter_value.hpp"
#include "rcl_interfaces/msg/parameter_type.hpp"
#include "rcl_interfaces/srv/set_parameters.hpp"

using SetP = rcl_interfaces::srv::SetParameters;
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
                    RCLCPP_INFO(this->get_logger(),"Request Success");
                }
                if(response->result == ServiceTurtleControl::Response::FAIL){
                    RCLCPP_ERROR(this->get_logger(),"Request Fail");
                }   
            });
        });
    }
        
        
    SetP::Response::SharedPtr call_set_parameters(const rcl_interfaces::msg::Parameter &param){
        auto param_client = this->create_client<SetP>("/TurtleControlNode/set_parameters");
       
        while(!param_client->wait_for_service(1s)){
            if(!rclcpp::ok()){
                RCLCPP_ERROR(this->get_logger(),"Fail to wait for server online, rclcpp stop");
                return nullptr;
            }
            RCLCPP_INFO(this->get_logger(),"Waiting for server online.....");
            srand(time(NULL));
        }

        auto request = std::make_shared<SetP::Request>();
        request->parameters.push_back(param);

        auto future = param_client->async_send_request(request);
        rclcpp::spin_until_future_complete(this->get_node_base_interface(),future);
        auto response = future.get();
        return response;
    }
    
    void update_server_param(double k){

        auto param = rcl_interfaces::msg::Parameter();
        param.name = "k";
        auto param_value = rcl_interfaces::msg::ParameterValue();
        param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value = k;
        param.value = param_value;

        auto response = this->call_set_parameters(param);
        if(response==NULL)
        {
            RCLCPP_INFO(this->get_logger(),"Param update failed");
            return;
        }
        for(auto result:response->results){
            if(result.successful==false){
                RCLCPP_INFO(this->get_logger(),"Param update failed : %s",result.reason.c_str());
            }
            else{
                RCLCPP_INFO(this->get_logger(),"Param update success");
            }
        }
    }


    
};

int main(int argc, char const *argv[])
{
    rclcpp::init(argc,argv);

    auto ClientControlNode_ = std::make_shared<ClientControlNode>("ClientControlNode");

    ClientControlNode_->update_server_param(4.0);
    rclcpp::spin(ClientControlNode_);

    rclcpp::shutdown();

    return 0;

    
}
