from sqlalchemy import Integer, String, BLOB, Column, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Clump class that lets us add to our sqlalchemy database
class Clump(Base):

    __tablename__ = 'Clumps'

    id = Column(Integer, primary_key=True)
    clump_name = Column(String)
    clump_mesh = Column(BLOB)

    # in kpc/Myr
    clump_x_velocity = Column(Float)
    clump_y_velocity = Column(Float)
    clump_z_velocity = Column(Float)

    # in kpc
    clump_x_loc = Column(Float)
    clump_y_loc = Column(Float)
    clump_z_loc = Column(Float)

    # in kpc
    clump_radius = Column(Float)

    # in Msun
    clump_mass = Column(Float)

    clump_original_index = Column(Integer)

    # time step
    clump_time_step = Column(Integer)

    clump_children = Column(String)
    clump_parents = Column(String)

    # Possible columns that we may want in the future

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
              "(clump_time_step={:d})>"\
              .format(self.clump_name,
                      x_vel, y_vel, z_vel,
                      x_loc, y_loc, z_loc,
                      self.clump_mass,
                      self.clump_time_step)
        return ret


engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

c1 = Clump(clump_name='c1', clump_time_step=0, clump_mass=0)
session.add(c1)
session.commit()
session.close()