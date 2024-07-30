# Dependencies
from flask import Flask, jsonify, Blueprint, make_response, request
import requests

# Other classes
from helpers.logger import *


api = Blueprint('api', __name__)

# The API Requets URL for "SpaceX API"
API_requests = "https://api.spacexdata.com/v4/" 

logger = log_messages()

def get_data(endpoint: str) -> (dict, int):
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
    logger.warning("Endpoint doesn't exist yet.")
    return {"message": "Dashboard endpoint not yet implemented"}, 501

@api.route('rockets', methods=["GET"])
def get_rockets():
    """
    Function to get all rockets and the status code
    """
    logger.info("Accessed /rockets endpoint")
    data, status_code = get_data("rockets")
    return make_response(jsonify(data), status_code)
    
@api.route('launches', methods=["GET"])
def get_launches():
    """
    Function to get all the launches
    """
    logger.info("Accessed /launches endpoint")
    data, status_code = get_data("launches")
    return make_response(jsonify(data), status_code)

@api.route('starlink', methods=["GET"])
def get_starlink():
    """
    Function to get all the starlink satellities
    """
    logger.info("Accessed /starlink endpoint")
    data, status_code = get_data("starlink")
    return make_response(jsonify(data), status_code)

@api.app_errorhandler(404)
def page_not_found(e):
    logger.error(f"Page not found: {request.url}")
    return jsonify(error="This resource was not found"), 404

@api.app_errorhandler(500)
def internal_server_error(e):
    logger.critical(f"Server error: {request.url} - {e}")
    return jsonify(error="An internal server error occurred"), 500