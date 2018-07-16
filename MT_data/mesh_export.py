import trimesh
from trimesh.io.export import export_mesh

def mesh_exporter(folder_location, mesh_name):
    orig_mesh = trimesh.load_mesh(folder_location + '/' + mesh_name)
    comps = orig_mesh.split()

    ind = 0
    for comp in comps:
        export_mesh(comp, folder_location + '/comp%i.obj' % ind)
        ind = ind + 1


mesh_exporter('DD0597_clumps', 'DD0597_all_clumps.obj')

mesh_exporter('DD0598_clumps', 'DD0598_all_clumps.obj')
