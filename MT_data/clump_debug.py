import yt, trimesh, numpy as np
# from trimesh.io.export import export_mesh

# import the base mesh and then split it into it's disconnected components
mesh = trimesh.load_mesh('trianglified.obj', 'obj')
mesh_components = mesh.split()

# load in the yt data
ds = yt.load('DD0600/DD0600')

ad = ds.r[(660, 'kpc'):(675, 'kpc'), :, :]


data_list = ad['x'], ad['y'], ad['z']
#print(np.stack(data_list).shape)
# clump0 = mesh_components[0]
# clump0_location = np.where(clump0.contains(np.stack(data_list).T))
# avg_mass = np.average(ad['particle_mass'][clump0_location].to_ndarray())
# print("Working clump location array: ")
# print(clump0_location[0])
# print(type(ad['particle_mass'][clump0_location]))

clump123 = mesh_components[123]
positions = np.stack(data_list).T
clump123_location = np.where(clump123.contains(positions))
print("Not working clump location array: ")
print(clump123_location[0])
#
# avg_mass = np.average(ad['cell_mass'][clump123_location].to_ndarray())
