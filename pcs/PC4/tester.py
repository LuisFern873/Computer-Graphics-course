from exercise01.solution import project_points
from exercise02.solution import sequence_of_projections
from exercise03.solution import draw_mesh_on_top_of_marker

def test_exercise01():

    project_points(
        full_path_input_mesh="meshes-for-exercises-1-2-3/bunny.off",
        optical_center_x=640, 
        optical_center_y=480, 
        optical_center_z=0,
        optical_axis_x=0, 
        optical_axis_y=0, 
        optical_axis_z=-150,
        focal_distance=800, 
        output_width_in_pixels=1280, 
        output_height_in_pixels=960,
        full_path_output="exercise01/bunny.png"
    )

    project_points(
        full_path_input_mesh="meshes-for-exercises-1-2-3/cow_mc-hr.off",
        optical_center_x=640, 
        optical_center_y=480, 
        optical_center_z=0,
        optical_axis_x=0, 
        optical_axis_y=0, 
        optical_axis_z=-10,
        focal_distance=800, 
        output_width_in_pixels=1280, 
        output_height_in_pixels=960,
        full_path_output="exercise01/cow_mc-hr.png"
    )


    project_points(
        full_path_input_mesh="meshes-for-exercises-1-2-3/gargoyle-10k-faces.off",
        optical_center_x=640, 
        optical_center_y=480, 
        optical_center_z=0.0,
        optical_axis_x=0, 
        optical_axis_y=0, 
        optical_axis_z=-2.0,
        focal_distance=800, 
        output_width_in_pixels=1280, 
        output_height_in_pixels=960,
        full_path_output="exercise01/gargoyle-10k-faces.png"
    )

def test_exercise02():
    sequence_of_projections(
        full_path_input_mesh="meshes-for-exercises-1-2-3/bunny.off",
        optical_center_x=[640 + i for i in range(0, 50, 5)], 
        optical_center_y=[480 for _ in range(10)], 
        optical_center_z=[0 for _ in range(10)],
        optical_axis_x=[i for i in range(0, 50, 5)], 
        optical_axis_y=[0,0,0,0,0,0,0,0,0,0], 
        optical_axis_z=[-150 for _ in range(10)],
        focal_distance=[800 for _ in range(10)], 
        output_width_in_pixels=1280, 
        output_height_in_pixels=960,
        prefix_output_files="exercise02/bunny"
    )


def test_exercise03():
    draw_mesh_on_top_of_marker(
        full_path_input_image='exercise03/input.jpg',
        full_path_mesh='meshes-for-exercises-1-2-3/cow_mc-hr.off',
        full_path_output_image='exercise03/cow_mc-hr.png'
    )

    draw_mesh_on_top_of_marker(
        full_path_input_image='exercise03/input.jpg',
        full_path_mesh='meshes-for-exercises-1-2-3/gargoyle-10k-faces.off',
        full_path_output_image='exercise03/gargoyle-10k-faces.png'
    )

    draw_mesh_on_top_of_marker(
        full_path_input_image='exercise03/input.jpg',
        full_path_mesh='meshes-for-exercises-1-2-3/bunny.off',
        full_path_output_image='exercise03/bunny.png'
    )

def test_exercise04():
    pass

def test_exercise05():
    pass

def test_exercise06():
    pass

if __name__ == "__main__":
    test_exercise01()
