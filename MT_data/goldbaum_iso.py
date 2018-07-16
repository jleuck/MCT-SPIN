import yt
from yt.units import g, cm

# load in the data
ds = yt.load("DD0600/DD0600")
# fields = ds.field_list


# run an isoountour extraction
# ad = ds.all_data()

# selecting a smaller subset of the data
ad = ds.r[(660, 'kpc'):(675, 'kpc'), :, :]
# print(ds.domain_right_edge.to('kpc'))

# from the parameters of the data in units m_h/cm**3

m_h = 1.67e-24

# star_maker_d_thresh = 50
star_maker_d_thresh = 50
rho = m_h * star_maker_d_thresh

# d_extrema = ad.quantities.extrema(('gas', 'density'))
# print(d_extrema)
# print(ds.field_list)
iso = ad.extract_isocontours(('gas', 'density'),
                             rho*g/cm**3,
                             'isocontours_test_small.obj')
print(iso)