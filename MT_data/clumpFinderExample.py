import yt
import numpy as np
from yt.analysis_modules.level_sets.api import *


ds = yt.load('IsolatedGalaxy/galaxy0030/galaxy0030')

disk = ds.disk([0.5, 0.5, 0.5], [1., 0, 0], (8, 'kpc'), (1, 'kpc'))

field = ('gas', 'density')

step = 2.0

c_min = 10**(np.log10(disk[field]).min())
c_max = 10**(np.log10(disk[field]).max())

master_clump = Clump(disk, field)

master_clump.add_validator('min_cells', 20)

find_clumps(master_clump, c_min, c_max, step)

ctree = master_clump.save_as_dataset('ClumpEx',
                                     fields=['density', 'particle_mass'])
# visualize the clumps
projection = yt.ProjectionPlot(ds, 2, field, center='c', width=(40, 'kpc'))

leaf_clumps = get_lowest_clumps(master_clump)
projection.annotate_clumps(leaf_clumps)
projection.save('clumps_projection')
