from sqlalchemy import create_engine, Column, Integer, String, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import numpy as np

engine = create_engine('sqlite:///AlchEx.db', echo=False)

Base = declarative_base()

class Clump(Base):
    __tablename__ = 'Clumps'

    clump_id = Column(Integer, primary_key=True)
    clump_name = Column(String)
    clump_file = Column(BLOB)

    def __repr__(self):
        return "<Clump(name='%s')>" % self.clump_name

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

session = Session()


name = 'clump001'

filename = 'comp1.obj'

with open(filename, 'rb') as f:
    data = f.read()

blob = data

clump1 = Clump(clump_name=name, clump_file=blob)

session.add(clump1)
session.commit()

our_clump = session.query(Clump).all()

print(our_clump)
