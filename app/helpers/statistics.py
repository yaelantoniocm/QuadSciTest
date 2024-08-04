from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from models import Rockets, Launches, Starlink
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
        total_rockets = session.query(func.count(Rockets.id)).scalar()
        avg_success_rate = session.query(func.avg(Rockets.success_rate_pct)).scalar()
        total_cost_per_launch = session.query(func.sum(Rockets.cost_per_launch)).scalar()
        avg_height = session.query(func.avg(Rockets.height_meters)).scalar()
        avg_diameter = session.query(func.avg(Rockets.diameter_meters)).scalar()
        return {
            "total_rockets": total_rockets,
            "avg_success_rate": avg_success_rate,
            "total_cost_per_launch": total_cost_per_launch,
            "avg_height": avg_height,
            "avg_diameter": avg_diameter
        }
    except Exception as e:
        # Log the error
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
        total_launches = session.query(func.count(Launches.id)).scalar()
        successful_launches = session.query(func.count(Launches.id)).filter(Launches.success == 'true').scalar()
        failed_launches = session.query(func.count(Launches.id)).filter(Launches.success == 'false').scalar()
        avg_launches_per_year = session.query(func.count(Launches.id) / func.count(func.distinct(func.extract('year', Launches.date_utc)))).scalar()
        most_used_rocket = session.query(Launches.rocket_id, func.count(Launches.rocket_id)).group_by(Launches.rocket_id).order_by(func.count(Launches.rocket_id).desc()).first()
        return {
            "total_launches": total_launches,
            "successful_launches": successful_launches,
            "failed_launches": failed_launches,
            "avg_launches_per_year": avg_launches_per_year,
            "most_used_rocket": {
                "rocket_id": most_used_rocket[0],
                "count": most_used_rocket[1]
            } if most_used_rocket else None
        }
    except Exception as e:
        # Log the error
        logger.error(f"Error retrieving launch statistics: {e}")
        # Raise the exception to be handled by the caller
        raise
    finally:
        session.close()

def get_launch_statistics():
    """
    Retrieve statistics related to launches from the database.

    Returns:
        dict: A dictionary containing launch statistics, including the total number of launches,
              number of successful and failed launches, average launches per year, and the most used rocket model.
    """
    session = Session()
    try:
        total_launches = session.query(func.count(Launches.id)).scalar()
        successful_launches = session.query(func.count(Launches.id)).filter(Launches.success == 'true').scalar()
        failed_launches = session.query(func.count(Launches.id)).filter(Launches.success == 'false').scalar()
        avg_launches_per_year = session.query(func.count(Launches.id) / func.count(func.distinct(func.extract('year', Launches.date_utc)))).scalar()
        most_used_rocket = session.query(Launches.rocket_id, func.count(Launches.rocket_id)).group_by(Launches.rocket_id).order_by(func.count(Launches.rocket_id).desc()).first()
        return {
            "total_launches": total_launches,
            "successful_launches": successful_launches,
            "failed_launches": failed_launches,
            "avg_launches_per_year": avg_launches_per_year,
            "most_used_rocket": most_used_rocket
        }
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
        total_satellites = session.query(func.count(Starlink.id)).scalar()
        active_satellites = session.query(func.count(Starlink.id)).filter(Starlink.decay_date == None).scalar()
        decayed_satellites = session.query(func.count(Starlink.id)).filter(Starlink.decay_date != None).scalar()
        return {
            "total_satellites": total_satellites,
            "active_satellites": active_satellites,
            "decayed_satellites": decayed_satellites
        }
    except Exception as e:
        # Log the error
        logger.error(f"Error retrieving Starlink statistics: {e}")
        # Raise the exception to be handled by the caller
        raise
    finally:
        session.close()