from sqlalchemy import create_engine, Column, String, Integer, Float, Date, inspect, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from config import DATABASE_URI

from helpers.logger import logger
# Declarative base for defining models
Base = declarative_base()

class Rockets(Base):
    """_summary_

    Args:
        Base (DeclarativeMeta): Base from which all ORM models inherit
    
    Attributes:
        id (str): Unique identifier for the rocket.
        name (str): Name of the rocket.
        success_rate_pct (float): Success rate of the rocket in percentage.
        cost_per_launch (int): Cost per launch in dollars.
        height_meters (float): Height of the rocket in meters.
        diameter_meters (float): Diameter of the rocket in meters.
        mass_kg (int): Mass of the rocket in kilograms.
        thrust_sea_level_kN (float): Thrust at sea level in kN.
        thrust_vacuum_kN (float): Thrust in vacuum in kN.
        first_flight (date): Date of the rocket's first flight.
    """
    __tablename__ = 'rockets'
    id = Column(String, primary_key = True)
    name = Column(String)
    success_rate_pct = Column(Float)
    cost_per_launch = Column(Integer)
    height_meters = Column(Float)
    diameter_meters = Column(Float)
    mass_kg = Column(Integer)
    thrust_sea_level_kN = Column(Float)
    thrust_vacuum_kN = Column(Float)
    first_flight = Column(Date)
    
    launches = relationship('Launches', back_populates='rocket')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'success_rate_pct': self.success_rate_pct,
            'cost_per_launch': self.cost_per_launch,
            'height_meters': self.height_meters,
            'diameter_meters': self.diameter_meters,
            'mass_kg': self.mass_kg,
            'thrust_sea_level_kN': self.thrust_sea_level_kN,
            'thrust_vacuum_kN': self.thrust_vacuum_kN,
            'first_flight': self.first_flight
        }
    
class Launches(Base):
    """SQLAlchemy model for the 'launches' table.
    
    Args:
        Base (DeclarativeMeta): Base class for all ORM models.
    
    Attributes:
        id (str): Unique identifier for the launch.
        name (str): Name of the launch.
        date_utc (date): Date of the launch in UTC.
        success (str): Success of the launch (True/False).
        rocket_id (str): Identifier of the rocket used.
        flight_number (int): Flight number.
    """
    __tablename__ = 'launches'
    id = Column(String, primary_key=True)
    name = Column(String)
    date_utc = Column(Date)
    success = Column(String)
    rocket_id = Column(String, ForeignKey('rockets.id'))
    flight_number = Column(Integer)
    
    
    rocket = relationship('Rockets', back_populates='launches')
    starlinks = relationship('Starlink', back_populates='launch')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_utc': self.date_utc,
            'success': self.success,
            'rocket_id': self.rocket_id,
            'flight_number': self.flight_number,
        }

class Starlink(Base):
    """SQLAlchemy model for the 'starlink' table.
    
    Args:
        Base (DeclarativeMeta): Base class for all ORM models.
    
    Attributes:
        id (str): Unique identifier for the satellite.
        object_name (str): Name of the satellite.
        launch_date (date): Launch date of the satellite.
        decay_date (date): Decay date of the satellite.
        inclination (float): Orbital inclination in degrees.
        apoapsis (float): Apoapsis altitude in km.
        periapsis (float): Periapsis altitude in km.
        launch_id (str): Identifier of the launch.
    """
    __tablename__ = 'starlink'
    id = Column(String, primary_key=True)
    object_name = Column(String)
    launch_date = Column(Date)
    decay_date = Column(Date)
    inclination = Column(Float)
    apoapsis = Column(Float)
    periapsis = Column(Float)
    launch_id = Column(String, ForeignKey('launches.id'))
    
    launch = relationship('Launches', back_populates='starlinks')
    
    def to_dict(self):
        return {
            'id': self.id,
            'object_name': self.object_name,
            'launch_date': self.launch_date,
            'decay_date': self.decay_date,
            'inclination': self.inclination,
            'apoapsis': self.apoapsis,
            'periapsis': self.periapsis,
            'launch_id': self.launch_id
        }
# Create the database engine
engine = create_engine(DATABASE_URI)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

def create_tables():
    """
    Create tables in the database based on the defined models if they do not exist.
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if not {'rockets', 'launches', 'starlink'}.issubset(tables):
        Base.metadata.create_all(engine)
        logger.info("Tables created.")
    else:
        logger.info("Tables already exist.")

if __name__ == "__main__":
    create_tables()