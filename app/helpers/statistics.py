from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from databases.models import Rockets, Launches, Starlink
from config import DATABASE_URI

from helpers.logger import logger
# Create the database engine and session factory
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def get_rocket_statistics():
    """
    Retrieve statistics related to rockets from the database.

    Returns:
        dict: A dictionary containing rocket statistics, including the total number of rockets,
              average success rate, total cost per launch, average height, and average diameter.
    """
    session = Session()
    try:
        rockets = session.query(Rockets).all()
        rocket_stats = {
            "total_rockets": len(rockets),
            "avg_success_rate": sum([rocket.success_rate_pct for rocket in rockets]) / len(rockets) if rockets else 0,
            "total_cost_per_launch": sum([rocket.cost_per_launch for rocket in rockets]),
            "avg_height": sum([rocket.height_meters for rocket in rockets]) / len(rockets) if rockets else 0,
            "avg_diameter": sum([rocket.diameter_meters for rocket in rockets]) / len(rockets) if rockets else 0
        }
        return rocket_stats
        # Log the error
    except Exception as e:
        logger.error(f"Error retrieving rocket statistics: {e}")
        # Raise the exception to be handled by the caller
        raise
    finally:
        session.close()

def get_launch_statistics():
    """
    Obtener estadísticas relacionadas con los lanzamientos de la base de datos.

    Returns:
        dict: Un diccionario que contiene estadísticas de los lanzamientos, incluyendo el número total de lanzamientos,
              el número de lanzamientos exitosos y fallidos, el promedio de lanzamientos por año y el modelo de cohete más utilizado.
    """
    session = Session()
    try:
        launches = session.query(Launches).all()
        launch_stats = {
            "total_launches": len(launches),
            "successful_launches": len([launch for launch in launches if launch.success == 'true']),
            "failed_launches": len([launch for launch in launches if launch.success == 'false']),
            "avg_launches_per_year": len(launches) / ((max([launch.date_utc for launch in launches]) - min([launch.date_utc for launch in launches])).days / 365) if launches else 0,
            "most_used_rocket": max(set([launch.rocket_id for launch in launches]), key=[launch.rocket_id for launch in launches].count) if launches else None
        }
        return launch_stats
    except Exception as e:
        # Log the error
        logger.error(f"Error retrieving launch statistics: {e}")
        # Raise the exception to be handled by the caller
        raise
    finally:
        session.close()
    
def get_starlink_statistics():
    """
    Obtener estadísticas relacionadas con los satélites Starlink de la base de datos.

    Returns:
        dict: Un diccionario que contiene estadísticas de los satélites Starlink, incluyendo el número total de satélites,
              el número de satélites activos y el número de satélites que han decaído.
    """
    session = Session()
    try:
        starlinks = session.query(Starlink).all()
        starlink_stats = {
            "total_satellites": len(starlinks),
            "active_satellites": len([satellite for satellite in starlinks if satellite.decay_date is None]),
            "decayed_satellites": len([satellite for satellite in starlinks if satellite.decay_date is not None])
        }
        return starlink_stats
    except Exception as e:
        # Log the error
        logger.error(f"Error retrieving Starlink statistics: {e}")
        # Raise the exception to be handled by the caller
        raise
    finally:
        session.close()