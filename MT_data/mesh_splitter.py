import trimesh
from trimesh.io.export import export_mesh
import os


# this function takes in a directory created by clump_extraction and fills it with the disconnected components
# within that mesh
# Useful for viewing interesting results
def get_mesh_components(directory):
    mesh = trimesh.load_mesh(directory + '/all_clumps.obj')
    try:
        mesh_components = mesh.split()
    except AttributeError:
        return

    index = 0
    for comp in mesh_components:
        file_name = directory + '/comp%i.obj' % index
        export_mesh(comp, file_name, 'obj')
        index = index +1