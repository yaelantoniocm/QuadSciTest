# Dependencies
from flask import Flask, jsonify, Blueprint, make_response, request
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# Other classes
from helpers.logger import logger
from models import Rockets, Launches, Starlink
from config import DATABASE_URI

# Crear el motor de base de datos y la sesión
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

api = Blueprint('api', __name__)

# The API Requets URL for "SpaceX API"
API_requests = "https://api.spacexdata.com/v4/" 

def get_data(endpoint: str):
    """
    Function to get data from the API
    """
    url = f"{API_requests}{endpoint}"
    try:
        response = requests.get(url)
        # To catch an HTTPError for bad responses
        response.raise_for_status()
        # To get the JSON data from the response
        data = response.json()
        logger.info(f"Successfully fetched data from {url}")
        return data, response.status_code
    
    # Handling specific HTTP errors
    except requests.exceptions.HTTPError as http_err:
        error_message = f"HTTP error occurred: {http_err}"
        logger.critical(error_message)
        return {"error": error_message}, response.status_code
    
    # Handling general request exceptions
    except requests.exceptions.RequestException as request_err:
        error_message = f"Request error occurred: {request_err}"
        logger.critical(error_message)
        return {"error": error_message}, 500
    
    # Handling any other exceptions
    except Exception as e:
        error_message = f"An error occurred: {e}"
        logger.critical(error_message)  # Registrar el error en el archivo log
        return {"error": error_message}, 500
    

@api.route('dashboard', methods=["GET"])
def get_dashboard():
    """
    Function to get the dashboards
    """
    logger.info("Accessed /dashboard endpoint")
    logger.critical("Endpoint /api/ doesn't exist yet.")
    return {"message": "Dashboard endpoint not yet implemented"}, 501

@api.route('rockets', methods=["GET"])
def get_rockets():
    """
    Function to get all rockets and the status code
    """
    logger.info("Accessed /rockets endpoint")
    try:
        data, status_code = get_data("rockets")
        logger.info(make_response(jsonify(data),status_code))
        return data, status_code
    except Exception as e:
        logger.error(f"Error in /rockets endpoint: {e}")
        return jsonify({"error": str(e)}), 500
    
@api.route('launches', methods=["GET"])
def get_launches():
    """
    Function to get all the launches
    """
    logger.info("Accessed /launches endpoint")
    try:
        data, status_code = get_data("launches")
        logger.info(make_response(jsonify(data),status_code))
        return data, status_code
    except Exception as e:
        logger.error(f"Error in /launches endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@api.route('starlink', methods=["GET"])
def get_starlink():
    """
    Function to get all the starlink satellities
    """
    logger.info("Accessed /starlink endpoint")
    try: 
        data, status_code = get_data("starlink")
        logger.info(make_response(jsonify(data),status_code))
        return data, status_code
    except Exception as e:
        logger.error(f"Error in /starlink endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@api.route('/rockets-clear', methods=['GET'])
def get_clear_rockets():
    """
    Function to get the clear data of the rockets form postgreSQL data base
    """
    session = Session()
    logger.info("Accessed /rockets-clear endpoint")
    try:
        rockets = session.query(Rockets).all()
        logger.info("Getting the clear data of rockets")
        return jsonify([rocket.to_dict() for rocket in rockets])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@api.route('/launches-clear', methods=['GET'])
def get_clear_launches():
    """
    Function to get the clear data of the launches form postgreSQL data base
    """
    session = Session()
    logger.info("Accessed /launches-clear endpoint")
    try:
        launches = session.query(Launches).all()
        logger.info("Getting the clear data of launches")
        return jsonify([launch.to_dict() for launch in launches])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@api.route('/starlink-clear', methods=['GET'])
def get__clear_starlink():
    """
    Function to get the clear data of the starlink satellites form postgreSQL data base
    """
    session = Session()
    logger.info("Accessed /starlink-clear endpoint")
    try:
        starlink = session.query(Starlink).all()
        logger.info("Getting the clear data of starlink")
        return jsonify([s.to_dict() for s in starlink])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@api.app_errorhandler(404)
def page_not_found(e):
    logger.error(f"Page not found: {request.url}")
    return jsonify(error="This resource was not found"), 404

@api.app_errorhandler(500)
def internal_server_error(e):
    logger.critical(f"Server error: {request.url} - {e}")
    return jsonify(error="An internal server error occurred"), 500