from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# Connect to Database and create database session
engine = create_engine('sqlite:///categorydata.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
