from sqlalchemy import create_engine, Column, Integer, String, BLOB, Float
from sqlalchemy.orm import sessionmaker
import json
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# this version of Clump doesn't use density
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
    # clump_density = Column(Float, default=0.)
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
              "(clump_time_step(Myr)={:d}),>"\
              .format(self.clump_name,
                      x_vel, y_vel, z_vel,
                      x_loc, y_loc, z_loc,
                      self.clump_mass,
                      self.clump_time_step)
        return ret
# returns a dict of all ids that the clump has had in the simulation
def get_clump_history(id, database_name):
    # get the clump object from the database
    db = 'sqlite:///' + database_name
    engine = create_engine(db)
    Session = sessionmaker(bind=engine)
    session = Session()

    clump = session.query(Clump).filter_by(id=id).first()
    if not clump:
        print('Invalid ID')
        return

    # add the current clump to the dictionary
    # now we will hard code in 600 as the number of entries, this should probably be changed in the future
    history = {}
    for i in range(601):
        history[i] = []
    history[clump.clump_time_step].append(id)

    # add all of the clump's children
    children = json.loads(clump.clump_children)
    for child in children:
        get_clump_future(child, history, session)

    # add all of the clump's parents
    parents = json.loads(clump.clump_parents)
    for parent in parents:
        get_clump_past(parent, history, session)

    return history


def get_clump_future(id, dict, session):
    # add current clump to dictionary
    clump = session.query(Clump).filter_by(id=id).first()
    dict[clump.clump_time_step].append(clump.id)

    # recurse on all children
    children = json.loads(clump.clump_children)
    for child in children:
        get_clump_future(child, dict, session)


def get_clump_past(id, dict, session):
    # add current clump to dictionary
    clump = session.query(Clump).filter_by(id=id).first()
    dict[clump.clump_time_step].append(clump.id)

    # recurse on all parents
    parents = json.loads(clump.clump_parents)
    for parent in parents:
        get_clump_past(parent, dict, session)

# id = 154
# database_name = 'clumps.db'
# dict = get_clump_history(id, database_name)
#
# for key in dict:
#     print(str(key) + ':' + str(dict[key]))
