import compas
from compas.datastructures import Mesh
from compas.geometry import smooth_centroid
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get_data('faces.obj'))

vertices = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
adjacency = mesh.halfedge
fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

lines = []
for u, v in mesh.edges():
    lines.append({
        'start': mesh.vertex_coordinates(u, 'xy'),
        'end'  : mesh.vertex_coordinates(v, 'xy'),
        'color': '#cccccc',
        'width': 1.0,
    })

smooth_centroid(vertices, adjacency, fixed=fixed, kmax=100)

plotter = MeshPlotter(mesh)

plotter.draw_xlines(lines)
plotter.draw_vertices()
plotter.draw_edges()

plotter.show()