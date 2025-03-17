import os

# Blender
FeatherBlender = 0
MultiBandBlender = 1
# features_finder
AKAZE = 0
ORB = 1
SIFT = 2
SURF = 3
# features_matcher
AffineBestOf2Nearest = 0
BestOf2NearestRange = 1
# warper
Affine = 0
CompressedRectilinearPortrait = 1 
CompressedRectilinear = 2
Cylindrical = 3 
Fisheye = 4 
Mercator = 5 
PaniniPortrait = 6
Panini = 7
Plane = 8
Spherical = 9
Stereographic = 10 
TransverseMercator = 11

# CHANGE local_path IN ANOTHER MACHINE 
local_path = "C:/Users/LENOVO/Desktop/Computer-Graphics-course/pcs/PC4/exercise04"
executable = "OpenCVProject1/x64/Release/OpenCVProject1.exe"

def stitch_images(full_path_input_image, blender, features_finder, features_matcher, warper, full_path_output_image):
    
    full_path_input_image = ",".join(full_path_input_image)

    command = f"{local_path}/{executable} {full_path_input_image} {blender} {features_finder} {features_matcher} {warper} {full_path_output_image}"

    print(command)
    os.system(command)

    print(f"{full_path_output_image} generated.")

# Test cases
stitch_images(
    full_path_input_image=[
        f"{local_path}/images-for-stitcher/panorama1-input-1.jpg",
        f"{local_path}/images-for-stitcher/panorama1-input-2.jpg",
        f"{local_path}/images-for-stitcher/panorama1-input-3.jpg",
        f"{local_path}/images-for-stitcher/panorama1-input-4.jpg",
        f"{local_path}/images-for-stitcher/panorama1-input-5.jpg",
        f"{local_path}/images-for-stitcher/panorama1-input-6.jpg"
    ],
    blender = MultiBandBlender,
    features_finder = SIFT,
    features_matcher = BestOf2NearestRange,
    warper = Mercator,
    full_path_output_image = "panorama1-mercator.jpg"
)


# Test cases
stitch_images(
    full_path_input_image=[
        f"{local_path}/images-for-stitcher-grail/grail00.jpg",
        f"{local_path}/images-for-stitcher-grail/grail01.jpg",
        f"{local_path}/images-for-stitcher-grail/grail02.jpg",
        f"{local_path}/images-for-stitcher-grail/grail03.jpg",
        f"{local_path}/images-for-stitcher-grail/grail04.jpg",
        f"{local_path}/images-for-stitcher-grail/grail05.jpg"
    ],
    blender = FeatherBlender,
    features_finder = ORB,
    features_matcher = AffineBestOf2Nearest,
    warper = Plane,
    full_path_output_image = "panorama-grail-plane.jpg"
)