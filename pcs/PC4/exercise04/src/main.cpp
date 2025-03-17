#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    cv::Mat img = cv::imread("test.png");
    if (img.empty()) {
        std::cerr << "Error al cargar la imagen." << std::endl;
        return -1;
    }
    cv::imshow("Imagen", img);
    cv::waitKey(0);
    return 0;
}
