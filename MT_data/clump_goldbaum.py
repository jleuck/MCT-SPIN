import yt
from yt.analysis_modules.level_sets.api import *
import numpy as np


# just using the clump finding tutorial as a guide
ds = yt.load('DD0600/DD0600')

field = ('gas', 'density')
# data_source = ds.all_data()

# should be around 20 kpc for the real thing
data_source = ds.disk([0.5, 0.5, 0.5], [0., 0., 1.], (5, 'kpc'), (1, 'kpc'))

step = 10.0

c_min = 10**np.floor(np.log10(data_source[field].min()))
c_max = 10**np.floor(np.log10(data_source[field].max()))

master_clump = Clump(data_source, field)

master_clump.add_validator('min_cells', 20)

find_clumps(master_clump, c_min, c_max, step)

ctree = master_clump.save_as_dataset(fields=['density', 'particle_mass'])

# visualize the clumps
# projection = yt.ProjectionPlot(ds, 2, field, center='c', width=(40, 'kpc'))
#
# leaf_clumps = get_lowest_clumps(master_clump)
# projection.annotate_clumps(leaf_clumps)
# projection.save('clumps_projection')
