#include <QApplication>
#include <QLabel>
#include <QString>
#include <QMainWindow>
#include <sstream>
#include <thread>
#include <rclcpp/rclcpp.hpp>
#include <status_interfaces/msg/systemstatus.hpp>

using SystemStatus = status_interfaces::msg::Systemstatus;

class SysStatusDisplay : public rclcpp::Node
{
public:
    SysStatusDisplay(QLabel* label) : Node("sys_status_display"), label_(label)
    {
        subscriber_ = this->create_subscription<SystemStatus>(
            "sys_status",
            10,
            [this](const SystemStatus::SharedPtr msg) {
                QString text = formatMessage(msg);
                // 线程安全更新
                QMetaObject::invokeMethod(label_, [this, text]() {
                    label_->setText(text);
                });
            }
        );
        
        // 显示初始消息
        label_->setText("等待数据...");
    }

private:
    QString formatMessage(const SystemStatus::SharedPtr& msg)
    {
        std::stringstream show_str;
        show_str << "============== New state visualization tool =========\n"
                 << "Data time stamp:\t" << msg->stamp.sec << "s\n"
                 << "Host name:\t\t" << msg->host_name << "\n"
                 << "CPU usage rate:\t\t" << msg->cpu_percentage << "%\n"
                 << "Memory usage rate:\t" << msg->memory_percentage << "%\n"
                 << "=============================================\n";
        
        return QString::fromStdString(show_str.str());
    }
    
    rclcpp::Subscription<SystemStatus>::SharedPtr subscriber_;
    QLabel* label_;
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    rclcpp::init(argc, argv);
    
    // 创建Qt窗口
    QMainWindow window;
    auto label = new QLabel(&window);
    label->setAlignment(Qt::AlignTop);
    window.setCentralWidget(label);
    window.resize(500, 400);
    window.setWindowTitle("System Status Display");
    window.show();
    
    // 创建ROS2节点
    auto node = std::make_shared<SysStatusDisplay>(label);
    
    // 启动ROS2 spin线程
    std::thread spin_thread([&]() {
        rclcpp::spin(node);
    });
    
    int result = app.exec();
    
    rclcpp::shutdown();
    spin_thread.join();
    
    return result;
}