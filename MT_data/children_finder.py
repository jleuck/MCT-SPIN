from translate_extrapolation import clump_mapper
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from clump_catalogue import Clump
from sqlalchemy.ext.declarative import declarative_base


# get clump mapping for the current time step
def get_children(database, data_location, cur_time):
    Base = declarative_base()
    clump_map = clump_mapper(database, cur_time, data_location)[0]
    engine = create_engine('sqlite:///' + database)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()


    for old_clump in clump_map:
        cur_children = json.loads(old_clump.clump_children)
        for new_clump in clump_map[old_clump]:
            # set the parents for the new clump
            # modified this to query the clump in the current session first
            new = session.query(Clump).filter_by(id=new_clump.id).first()
            cur_parents = json.loads(new.clump_parents)
            cur_parents.append(old_clump.id)
            new_parents = json.dumps(cur_parents)

            new.clump_parents = new_parents
            session.commit()

            cur_children.append(new_clump.id)
        # set the children for the old clump
        old_children = json.dumps(cur_children)
        q = session.query(Clump).filter_by(id=old_clump.id).first()
        q.clump_children = old_children
        session.commit()

# database = 'big_clumps.db'
# data_location = 'DD0597/DD0597'
# cur_time = 597
#
# for i in range(3):
#     get_children(database, data_location, cur_time)
#     cur_time = cur_time + 1


def clear_children(database):
    engine = create_engine('sqlite:///' + database)
    Session = sessionmaker(bind=engine)
    session = Session()

    q = session.query(Clump).all()
    for clump in q:
        clump.clump_children = '[]'
        clump.clump_parents = '[]'
        session.commit()

# clear_children('clumps.db')