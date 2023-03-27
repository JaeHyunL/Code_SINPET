from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create the engine and session
engine = create_engine('postgresql://username:password@localhost/mydatabase')
Session = sessionmaker(bind=engine)
session = Session()

# create a base class for declarative models
Base = declarative_base()

# define the model class
class MyTable(Base):
    __tablename__ = 'mytable'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# define the data to upsert
data = {'id': 1, 'name': 'John'}

# perform the upsert
record = MyTable(**data)
session.merge(record)
session.commit()
