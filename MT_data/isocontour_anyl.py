import pymesh, numpy as np


# creates a mesh that contains the faces of the triangle mesh
def trianglify(m):
    vertices = m.vertices
    faces = list()
    face = list()
    for i in range(m.num_vertices):
        face.append(i)
        if i % 3 == 2:
            faces.append(face)
            face = list()
    faces = np.array(faces)
    new_mesh = pymesh.form_mesh(vertices, faces)
    return new_mesh


# load in the isocontour data
mesh1 = pymesh.load_mesh('isocontours_small.obj')
triangle_mesh = trianglify(mesh1)
pymesh.save_mesh('trianglified.obj', triangle_mesh)

# separate the disconnected mesh into it's disconnected components
disconnected = pymesh.separate_mesh(triangle_mesh, 'vertex')
for i in range(len(disconnected)):
    if(i < 25):
        print(len(disconnected[i].faces))

# def trianglify(m):
#     vertices = m.vertices
#     for(vertex: vertices)
