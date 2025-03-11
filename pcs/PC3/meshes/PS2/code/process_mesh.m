clear all;
close all;

addpath('../data/');
addpath('../external/');

% Name of the shape we are considering
shapename = 'torus_simple';
    
% Read the shape from an 'off' file
S = read_off_shape([shapename '.off']);

fprintf('Read mesh %s with %d vertices\n', shapename, size(S.surface.X, 1));

plot_mesh(S.surface);

%% PART I.
% Compute the Euler characteristic (to complete)
chi = euler_characteristic(S);

% Compute the degrees of all the vertices of the mesh
degrees = vertex_degrees(S);

% Verify that the number of edges = 2*avg_degree*number of vertices

%% PART II.
remove_vertices = 500;

for i=1:remove_vertices
    % Perform mesh simplification.
end
