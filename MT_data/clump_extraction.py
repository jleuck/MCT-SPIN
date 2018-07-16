import yt, trimesh
from yt.units import kpc, g, cm
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
from trimesh.io.export import export_mesh
from sqlalchemy import Integer, String, BLOB, Column, Float
from sqlalchemy.ext.declarative import declarative_base
from json import dumps

Base = declarative_base()


# Clump class that lets us add to our sqlalchemy database
class Clump(Base):

    __tablename__ = 'Clumps'

    id = Column(Integer, primary_key=True)
    clump_name = Column(String, default='clump')
    clump_mesh = Column(BLOB)

    # in kpc/Myr
    clump_x_velocity = Column(Float, default=0.)
    clump_y_velocity = Column(Float, default=0.)
    clump_z_velocity = Column(Float, default=0.)

    # in kpc
    clump_x_loc = Column(Float, default=0.)
    clump_y_loc = Column(Float, default=0.)
    clump_z_loc = Column(Float, default=0.)

    # in kpc
    clump_radius = Column(Float, default=0.)

    # in Msun
    clump_mass = Column(Float, default=0.)

    clump_original_index = Column(Integer, default=0)

    # time step
    clump_time_step = Column(Integer, default=0)

    clump_children = Column(String, default='[]')
    clump_parents = Column(String, default='[]')

    # Possible columns that we may want in the future
    # density in g/cm**3
    clump_density = Column(Float, default=0.)
    # star_formation_rate
    #

    def __repr__(self):
        x_vel = self.clump_x_velocity
        y_vel = self.clump_y_velocity
        z_vel = self.clump_z_velocity

        x_loc = self.clump_x_loc
        y_loc = self.clump_y_loc
        z_loc = self.clump_z_loc

        ret = "Clump<(clump_name={})," \
              "(clump_velocity(kpc/Myr)=[{:f}, {:f}, {:f}])," \
              "(clump_loc(kpc)=[{:f}, {:f}, {:f}])," \
              "(clump_mass(Msun)={:f})," \
              "(clump_time_step(Myr)={:d})," \
              "(clump_density(g/cm**3)={:f}>"\
              .format(self.clump_name,
                      x_vel, y_vel, z_vel,
                      x_loc, y_loc, z_loc,
                      self.clump_mass,
                      self.clump_time_step,
                      self.clump_density)
        return ret


def catalogue_maker(ds, database_name, mesh_components):
    # create the engine that we will use for our db
    engine = create_engine(database_name)

    # start session
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    # go through all of the components and add their information to the table
    index = 0
    orig_index = 0
    for clump in mesh_components:
        name = 'clump%i' % index
        file_loc = 'clumps/clump%i.obj' % index

        #setting up our yt spheres to check intersections with amr zones
        try:
            radius = clump.bounding_sphere.primitive.radius
            center = clump.bounding_sphere.primitive.center
        except ZeroDivisionError:
            radius = 0
            print('ZeroDivisionError on original index %i' % orig_index)

        if radius > ds.index.get_smallest_dx():

            sp = ds.sphere(center, radius)

            # exclude the smaller zones
            mass = sp['cell_mass'].to('Msun').to_ndarray()
            if mass.size > 30:

                    tot_mass = np.sum(mass)

                    # get bulk velocity of our sphere object
                    bulk_velocity = sp.quantities.bulk_velocity().to('kpc/Myr')
                    x_vel = bulk_velocity[0]
                    y_vel = bulk_velocity[1]
                    z_vel = bulk_velocity[2]

                    # get center of mass of our sphere object
                    cm = sp.quantities.center_of_mass().to('kpc')
                    x_loc = cm[0]
                    y_loc = cm[1]
                    z_loc = cm[2]

                    radius = ds.quan(radius, 'code_length').to('kpc')

                    # get average desnity weighted by cell mass
                    density = sp.quantities.weighted_average_quantity('Density', ('gas', 'cell_mass')).to('g/cm**3')

                    # get the time step from the data
                    time_step = np.round(ds.current_time.to('Myr'))

                    # set up the children and parent arrays
                    empty_ar = []
                    empty_ar = dumps(empty_ar)

                    export_mesh(clump, file_loc, 'obj')


                    #@TODO change this to 64 bit string encoding instead of blob
                    # also might not have to always export mesh first
                    with open(file_loc, 'rb') as file:
                        data = file.read()
                    blob = data

                    # create clump object and add it to the table
                    c = Clump(clump_name=name, clump_mesh=blob,
                              clump_x_velocity=x_vel, clump_y_velocity=y_vel, clump_z_velocity=z_vel,
                              clump_x_loc=x_loc, clump_y_loc=y_loc, clump_z_loc=z_loc,
                              clump_mass=tot_mass,
                              clump_radius=radius,
                              clump_density=density,
                              clump_original_index=orig_index,
                              clump_time_step=time_step,
                              clump_children=empty_ar,
                              clump_parents=empty_ar)
                    session.add(c)
                    session.commit()
                    index = index + 1
        orig_index = orig_index + 1

    session.close()


# function to extract clumps from a data set
def extract_clumps(ds, filename, database_name='clumps.db', verbose=False, big=False):
    if verbose:
        print('Creating region for ' + filename + '...')
    obj_filename = filename + '/all_clumps.obj'
    # we will hard code in the region for now, ideally this would encompass all of the relevant data
    domain_center = ds.domain_center
    if big:
        domain_le = ds.domain_center - 20*kpc
    else:
        domain_le = ds.domain_center
    domain_re = domain_center + 20*kpc
    region = ds.box(domain_le, domain_re)

    # do the isocontour extraction
    # density threshold is hardcoded, but based on StarMakerOverDensityThreshold of this simulation
    m_h = 1.67e-24
    d_thresh = 50
    rho = m_h * d_thresh
    if verbose:
        print('Extracting isocontours for ' + filename + '...')
    region.extract_isocontours(('gas', 'density'), rho*g/cm**3, obj_filename)

    # load in the mesh with trimesh and split it into it's components
    if verbose:
        print('Splitting mesh for ' + filename + '...')
    mesh = trimesh.load_mesh(obj_filename)
    if type(mesh) == list:
        if verbose:
            print('No isocontours found for ' + filename)
        return
    mesh_components = mesh.split()

    if verbose:
        print('Creating catalogue for ' + filename + '...')
    # create a database for these components
    database_name = 'sqlite:///clump_data.db'
    if big:
        database_name = 'sqlite:///clump_data.db'
    catalogue_maker(ds, database_name, mesh_components)


# toggle comments on the next two sections for a larger vs. smaller data set
# ts = yt.load('DD0???/DD0???')
# num = 597
# for ds in ts:
#     name = 'DD0%i' % num
#     extract_clumps(ds, name, verbose=True, big=True)
#     num = num + 1


# ts = yt.load('DD0???/DD0???')
# num = 597
# for ds in ts:
#     name = 'DD0%i_big' % num
#     extract_clumps(ds, name, verbose=True, big=True)
#     num = num + 1