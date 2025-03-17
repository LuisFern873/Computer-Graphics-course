#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <opencv2/stitching.hpp>
#include <opencv2/features2d.hpp>
#include <opencv2/core.hpp>

// Blender types
const int FeatherBlender = 0;
const int MultiBandBlender = 1;

// Features finder types
const int AKAZE = 0;
const int ORB = 1;
const int SIFT = 2;
const int SURF = 3;

// Features matcher types
const int AffineBestOf2Nearest = 0;
const int BestOf2NearestRange = 1;

// Warper types
const int Affine = 0;
const int CompressedRectilinearPortrait = 1;
const int CompressedRectilinear = 2;
const int Cylindrical = 3;
const int Fisheye = 4;
const int Mercator = 5;
const int PaniniPortrait = 6;
const int Panini = 7;
const int Plane = 8;
const int Spherical = 9;
const int Stereographic = 10;
const int TransverseMercator = 11;

void stitch_images(
    std::vector<std::string> full_path_input_image,
    int blender,
    int features_finder,
    int features_matcher,
    int warper,
    std::string full_path_output_image
) {
    std::vector<cv::Mat> images;

    for (const std::string& path : full_path_input_image) {
        cv::Mat image = cv::imread(path);
        if (image.empty()) {
            std::cerr << "Could not open or find the image at " << path << std::endl;
            return;
        }
        images.push_back(image);
    }

    // Create Stitcher instance
    cv::Ptr<cv::Stitcher> stitcher = cv::Stitcher::create(cv::Stitcher::PANORAMA);

    cv::Ptr<cv::detail::Blender> b;
    cv::Ptr<cv::Feature2D> ff;
    cv::Ptr<cv::detail::FeaturesMatcher> fm;
    cv::Ptr<cv::WarperCreator> w;

    if (blender == FeatherBlender) {
        b = cv::detail::FeatherBlender::createDefault(1);
    }
    else if (blender == MultiBandBlender) {
        b = cv::detail::MultiBandBlender::createDefault(2);
    }
    else {
        std::cerr << "Unrecognized blender type!" << std::endl;
        return;
    }

    if (features_finder == AKAZE) {
        ff = cv::AKAZE::create();
    }
    else if (features_finder == ORB) {
        ff = cv::ORB::create();
    }
    else if (features_finder == SIFT) {
        ff = cv::SIFT::create();
    }
    else if (features_finder == SURF) {
        // ff = cv::xfeatures2d::SURF::create();
        std::cerr << "SURF is not supported!" << std::endl;
        return;
    }
    else {
        std::cerr << "Unrecognized features finder type!" << std::endl;
        return;
    }

    if (features_matcher == AffineBestOf2Nearest) {
        fm = cv::makePtr<cv::detail::AffineBestOf2NearestMatcher>();
    }
    else if (features_matcher == BestOf2NearestRange) {
        fm = cv::makePtr<cv::detail::BestOf2NearestRangeMatcher>();
    }
    else {
        std::cerr << "Unrecognized features matcher type!" << std::endl;
        return;
    }

    float warper_scale = 1.0;

    switch (warper) {
    case Affine:
        w = cv::makePtr<cv::AffineWarper>();
        break;
    case CompressedRectilinearPortrait:
        w = cv::makePtr<cv::CompressedRectilinearPortraitWarper>(warper_scale);
        break;
    case CompressedRectilinear:
        w = cv::makePtr<cv::CompressedRectilinearWarper>(warper_scale);
        break;
    case Cylindrical:
        w = cv::makePtr<cv::CylindricalWarper>();
        break;
    case Fisheye:
        w = cv::makePtr<cv::FisheyeWarper>();
        break;
    case Mercator:
        w = cv::makePtr<cv::MercatorWarper>();
        break;
    case PaniniPortrait:
        w = cv::makePtr<cv::PaniniPortraitWarper>(warper_scale);
        break;
    case Panini:
        w = cv::makePtr<cv::PaniniWarper>(warper_scale);
        break;
    case Plane:
        w = cv::makePtr<cv::PlaneWarper>();
        break;
    case Spherical:
        w = cv::makePtr<cv::SphericalWarper>();
        break;
    case Stereographic:
        w = cv::makePtr<cv::StereographicWarper>();
        break;
    case TransverseMercator:
        w = cv::makePtr<cv::TransverseMercatorWarper>();
        break;
    default:
        std::cerr << "Unrecognized warper type!" << std::endl;
        return;
    }

    stitcher->setBlender(b);
    stitcher->setFeaturesFinder(ff);
    stitcher->setFeaturesMatcher(fm);
    stitcher->setWarper(w);

    // Output image
    cv::Mat pano;

    // Stitch the images
    cv::Stitcher::Status status = stitcher->stitch(images, pano);

    if (status != cv::Stitcher::OK) {
        std::cerr << "Can't stitch images, error code = " << int(status) << std::endl;
        return;
    }

    // Save the result
    cv::imwrite(full_path_output_image, pano);

    std::cout << "Done!" << std::endl;
}

int main(int argc, char** argv) {
    if (argc != 7) {
        std::cerr << "Usage: " << argv[0] << " <input_images> <blender> <features_finder> <features_matcher> <warper> <output_image>" << std::endl;
        return -1;
    }

    std::vector<std::string> full_path_input_image;
    std::istringstream ss(argv[1]);
    std::string path;
    while (std::getline(ss, path, ',')) {
        full_path_input_image.push_back(path);
    }

    int blender = std::stoi(argv[2]);
    int features_finder = std::stoi(argv[3]);
    int features_matcher = std::stoi(argv[4]);
    int warper = std::stoi(argv[5]);
    std::string full_path_output_image = argv[6];



    stitch_images(full_path_input_image, blender, features_finder, features_matcher, warper, full_path_output_image);

    std::cout << "Hello!" << std::endl;

    
    return 0;
}
