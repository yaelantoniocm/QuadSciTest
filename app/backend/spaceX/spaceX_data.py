# Dependencies
import requests

# From internal clases
from helpers import logger
from constants import SPACEX_API_URL

API_requests = "https://api.spacexdata.com/v4/" 

def get_data(endpoint: str):
    """
    Function to get data from the API SpaceX (here is raw data)
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