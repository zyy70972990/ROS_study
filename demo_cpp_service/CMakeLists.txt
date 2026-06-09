# cmake_minimum_required(VERSION 3.8)
# project(demo_cpp_service)

# if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
#   add_compile_options(-Wall -Wextra -Wpedantic)
# endif()


# # find dependencies
# find_package(ament_cmake REQUIRED)
# find_package(rclcpp REQUIRED)
# find_package(geometry_msgs REQUIRED)
# find_package(turtlesim REQUIRED)
# find_package(sensor_msgs REQUIRED)
# find_package(rosidl_default_generators REQUIRED)






# rosidl_generate_interfaces(${PROJECT_NAME}
#   "srv/TurtleControl.srv"
#   DEPENDENCIES sensor_msgs
# )

# add_executable(Service_Turtle_Control src/ServiceTurtleControl.cpp)
# ament_target_dependencies(Service_Turtle_Control rclcpp geometry_msgs turtlesim)


# if(BUILD_TESTING)
#   find_package(ament_lint_auto REQUIRED)
#   # the following line skips the linter which checks for copyrights
#   # comment the line when a copyright and license is added to all source files
#   set(ament_cmake_copyright_FOUND TRUE)
#   # the following line skips cpplint (only works in a git repo)
#   # comment the line when this package is in a git repo and when
#   # a copyright and license is added to all source files
#   set(ament_cmake_cpplint_FOUND TRUE)
#   ament_lint_auto_find_test_dependencies()
# endif()

# install(TARGETS Service_Turtle_Control
# DESTINATION lib/${PROJECT_NAME})

# ament_package()


cmake_minimum_required(VERSION 3.8)
project(demo_cpp_service)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# 查找依赖
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(turtlesim REQUIRED)      # 如果确实需要
find_package(sensor_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# ===== 关键：先生成服务接口 =====
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/TurtleControl.srv"
  DEPENDENCIES sensor_msgs   # 如果 .srv 中没有 sensor_msgs 类型可删除
)

# 再添加可执行文件
add_executable(Service_Turtle_Control src/ServiceTurtleControl.cpp)
add_executable(Client_Turtle_Control src/ClientTurtleControl.cpp)

# 链接依赖（包括生成的接口库）
target_link_libraries(Service_Turtle_Control
  ${PROJECT_NAME}__rosidl_generator_cpp
)

target_link_libraries(Service_Turtle_Control
  ${PROJECT_NAME}__rosidl_generator_cpp
  ${PROJECT_NAME}__rosidl_typesupport_cpp
)

target_link_libraries(Client_Turtle_Control
  ${PROJECT_NAME}__rosidl_generator_cpp
  ${PROJECT_NAME}__rosidl_typesupport_cpp
)

# 使用 ament_target_dependencies 处理其他常规依赖
ament_target_dependencies(Service_Turtle_Control
  rclcpp
  geometry_msgs
  turtlesim   # 可选
)

ament_target_dependencies(Client_Turtle_Control
  rclcpp
)

# 可选：显式包含生成的头文件目录（通常自动，但为了保险）
target_include_directories(Service_Turtle_Control PRIVATE
  ${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_cpp
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

# 安装到正确路径
install(TARGETS Service_Turtle_Control Client_Turtle_Control
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY launch
DESTINATION share/${PROJECT_NAME})
ament_package()