cmake_minimum_required(VERSION 3.10)

project(ImageStitcher)

set(OpenCV_DIR C:/Users/LENOVO/Desktop/Computer-Graphics-course/pcs/PC4/exercise04/OpenCV-MinGW-Build-OpenCV-4.5.5-x64/build)


find_package(OpenCV REQUIRED)

add_executable(${PROJECT_NAME} src/main.cpp)

target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
