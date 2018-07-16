import clump_extraction
import os
import yt
import numpy as np

yt.funcs.mylog.setLevel(25)
yt.enable_parallelism()

# make a directory to store all of our data
if not os.path.exists('Clump_Data'):
    os.makedirs('Clump_Data')

# data_location = '/dpool/goldbaum2016a/feedback_20pc/simulation_outputs/DD????/DD????'
# data_location = 'DD0???/DD0???'

# load in the time series data
# ts = yt.DatasetSeries(data_location)
ts = yt.DatasetSeries(['DD0597/DD0597', 'DD0598/DD0598'])
# ts = yt.DatasetSeries(['DD0597/DD0597'])

# bool that we can toggle to overwrite all data
overwrite = False

for ds in ts.piter():
    filename = 'D_' + str(int(np.rint(ds.current_time.to('Myr'))))
    path = 'Clump_Data/' + filename
    if not os.path.exists(path):
        os.makedirs(path)
        clump_extraction.extract_clumps(ds, path, database_name='Clump_Data/clumps.db',
                                        verbose=True, big=True)




