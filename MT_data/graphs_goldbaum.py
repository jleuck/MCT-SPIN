import yt
# from yt.units import kpc

ds = yt.load('DD0600/DD0600')
dd = ds.r[0.5:0.8]

prj = yt.ProjectionPlot(ds, 'z', 'Density')
# dd = ds.all_data()


rho = dd.quantities['WeightedAverageQuantity']('Density', 'cell_mass')
print(rho)
prj.save()
