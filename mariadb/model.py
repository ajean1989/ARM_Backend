from config import *

from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Table "_user"
class User(Base):
    __tablename__ = 'user'

    id_user = Column(Integer, primary_key=True)
    username = Column(String(64))
    last_name = Column(String(64))
    first_name = Column(String(64))
    gender = Column(Integer) # 0 : NR, 1 : H, 2: F, 3 : A
    age = Column(Integer)

    scans = relationship('Scan', back_populates='user')

class Item(Base):
    __tablename__ = 'item'

    id_code = Column(String(256), primary_key=True)
    brand = Column(Text)
    name = Column(Text)
    ingredient = Column(Text)
    allergen = Column(Text)
    nutriment = Column(Text)
    nutriscore = Column(Text)
    ecoscore = Column(Text)
    packaging = Column(Text)
    image = Column(String(256))
    url_openfoodfact = Column(String(512))

    scans = relationship('Scan', back_populates='item')

class Place(Base):
    __tablename__ = 'place'

    id_place = Column(Integer, primary_key=True)
    name = Column(String(64))
    Adresse = Column(String(128))
    Postcode = Column(Integer)
    city = Column(String(64))

    scans = relationship('Scan', back_populates='place')


# Table de jonction Many-to-Many
class Scan(Base):
    __tablename__ = 'scan'

    id_place = Column(Integer, ForeignKey('place.id_place'), primary_key=True)
    id_code = Column(String(256), ForeignKey('item.id_code'), primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id_user'), primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    hour = Column(Integer)
    minute = Column(Integer)

    # Définir les relations Many-to-One
    place = relationship('Place', back_populates='scan')
    item = relationship('Item', back_populates='scan')
    user = relationship('User', back_populates='scan')

# Ajouter les tables à la base de données
Base.metadata.create_all(engine)

# Créer une session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session()

