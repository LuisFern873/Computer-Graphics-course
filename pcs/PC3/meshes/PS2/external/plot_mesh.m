function plot_mesh(shape)
    trimesh(shape.TRIV, shape.X, shape.Y, shape.Z, ...
        'EdgeColor', 'k', 'FaceColor', 'interp');
    axis equal;
    axis off;
end