# Dependencies
from flask import Flask, jsonify, Blueprint, make_response, request, render_template_string
import requests

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Other classes
from helpers.logger import logger
from helpers.statistics import get_rocket_statistics, get_launch_statistics, get_starlink_statistics
from config import DATABASE_URI

from backend.starlink_resources.starlink_filter_sort import get_filter_sort_starlink
from backend.rocket_resources.rocket_filter_sort import get_filter_sort_rocket
from backend.launches_resources.launches_filter_sort import get_filter_sort_launches

# Create the database engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

api = Blueprint('api', __name__)

# The API Requets URL for "SpaceX API"
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
    

@api.route('/dashboard', methods=["GET"])
@api.route('/dashboard/<response_type>', methods=['GET'])
def get_dashboard(response_type=None):
    """
    Endpoint to get the dashboard with statistics.
    """
    logger.info("Accessed /dashboard endpoint")
    
    try: 
        rocket_stats = get_rocket_statistics()
        launch_stats = get_launch_statistics()
        starlink_stats = get_starlink_statistics()
        
        # Combine all stats into a single dictionary.
        dashboard_data = {
            "rockets": rocket_stats,
            "launches": launch_stats,
            "starlink": starlink_stats
        }
        if response_type == 'html':
            logger.info("Returning data dashboard in HTML format")
            return render_template_string("""
                <style>
                    table {
                        border-collapse: collapse;
                        width: 80%;
                        margin: auto;
                        text-align: center;
                    }
                    th, td {
                        padding: 8px;
                        border: 1px solid black;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                    .center {
                        text-align: center;
                    }
                </style>
                <h1 class="center">Dashboard Statistics</h1>
                <h2 class="center">Rocket Statistics</h2>
                <table>
                    <tr>
                        <th>Total Rockets</th>
                        <th>Avg Success Rate (%)</th>
                        <th>Total Cost Per Launch ($)</th>
                        <th>Avg Height (m)</th>
                        <th>Avg Diameter (m)</th>
                    </tr>
                    <tr>
                        <td>{{ rockets.total_rockets }}</td>
                        <td>{{ rockets.avg_success_rate }}</td>
                        <td>{{ rockets.total_cost_per_launch }}</td>
                        <td>{{ rockets.avg_height }}</td>
                        <td>{{ rockets.avg_diameter }}</td>
                    </tr>
                </table>
                <h2 class="center">Launch Statistics</h2>
                <table>
                    <tr>
                        <th>Total Launches</th>
                        <th>Successful Launches</th>
                        <th>Failed Launches</th>
                        <th>Avg Launches Per Year</th>
                        <th>Most Used Rocket</th>
                    </tr>
                    <tr>
                        <td>{{ launches.total_launches }}</td>
                        <td>{{ launches.successful_launches }}</td>
                        <td>{{ launches.failed_launches }}</td>
                        <td>{{ launches.avg_launches_per_year }}</td>
                        <td>{{ launches.most_used_rocket }}</td>
                    </tr>
                </table>
                <h2 class="center">Starlink Statistics</h2>
                <table>
                    <tr>
                        <th>Total Satellites</th>
                        <th>Active Satellites</th>
                        <th>Decayed Satellites</th>
                    </tr>
                    <tr>
                        <td>{{ starlink.total_satellites }}</td>
                        <td>{{ starlink.active_satellites }}</td>
                        <td>{{ starlink.decayed_satellites }}</td>
                    </tr>
                </table>
            """, rockets=rocket_stats, launches=launch_stats, starlink=starlink_stats)
        # Give the data in JSON format
        elif response_type is None or response_type == 'json':
            logger.info("Returning data dashboard in JSON format.")
            return jsonify(dashboard_data)
    except Exception as e:
        logger.error(f"Error in /dashboard endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@api.route('rockets-raw', methods=["GET"])
def get_rockets():
    """
    Function to get all rockets and the status code(200,300,400,500)

    Returns:
        GET: Return all the data of rockets in JSON format 
    """
    logger.info("Accessed /rockets endpoint")
    try:
        data, status_code = get_data("rockets")
        logger.info(make_response(jsonify(data),status_code))
        return data, status_code
    except Exception as e:
        logger.error(f"Error in /rockets endpoint: {e}")
        return jsonify({"error": str(e)}), 500
    
@api.route('launches-raw', methods=["GET"])
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

@api.route('starlink-raw', methods=["GET"])
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

@api.route('/rockets', methods=['GET'])
@api.route('/rockets/<response_type>', methods=['GET'])
def get_clear_rockets(response_type=None):
    """
    Endpoint to get rocket data with optional filtering and sorting.

    Args:
    response_type (string, optional (JSON or HTML)): Response type ('html' or 'json'). If not specified, returns JSON.

    Returns:
    JSON or HTML: Rocket data in the specified format.
    
    Examples of querys:
    
    api/rockets/json?filter_field=first_flight&filter_value=2020&sort_low=cost_per_launch
    
    api/rockets?filter_field=id&filter_value=5eb87cdcffd86e000604b32a
    
    api/rockets/html?filter_field=first_flight&filter_value=2010&sort_high=height_meters

    Query format:
    
    api/rockets?filter_field={filter_field}&filter_value={possible_filter_value}&sort_low={sort_high / sort_low}
    
    api/rockets/{format}?filter_field={filter_field}&filter_value={possible_filter_value}&sort_low={sort_high / sort_low}
    
    Can sort any value except id and can filter any value.
    
    The format is json or html.
    """
    session = Session()
    logger.info("Accessed /rockets-clear endpoint")

    try:
        # Get sorting and filtering parameters from the request
        sort_param = request.args.get('sort_high') or request.args.get('sort_low')
        sort_order = 'desc' if request.args.get('sort_high') else 'asc'
        filter_field = request.args.get('filter_field')
        filter_value = request.args.get('filter_value')
        
        # Validate that both filtering parameters are present
        if (filter_field and not filter_value) or (not filter_field and filter_value):
            logger.error("Both filter_field and filter_value must be provided for filtering.")
            return jsonify({"error": "Both filter_field and filter_value must be provided for filtering."}), 400
        
        # Get rocket data by applying filtering and sorting if specified
        rockets = get_filter_sort_rocket(session, sort_param, sort_order, filter_field, filter_value)
        
        # In case rockets with the filtering specifications are not found
        if not rockets:
            logger.error("No rockets found matching the specifications")
            return jsonify({"message": "No rockets found matching the specifications"}), 404
        
        logger.info("Getting the processed data of rockets")
        
        # Give the data in a HTML table format
        if response_type == 'html':
            logger.info("Returning data of rockets in HTML format")
            return render_template_string("""
                <html>
                <head>
                    <style>
                        table, h1 {
                            border-collapse: collapse;
                            width: 80%;
                            margin: auto;
                            text-align: center;
                        }
                        th, td {
                            padding: 8px;
                            border: 1px solid black;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                    </style>
                </head>
                <body>
                    <h1>Rockets</h1> <!-- Table title -->
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Success Rate (%)</th>
                            <th>Cost per Launch</th>
                            <th>Height (m)</th>
                            <th>Diameter (m)</th>
                            <th>Mass (kg)</th>
                            <th>Thrust Sea Level (kN)</th>
                            <th>Thrust Vacuum (kN)</th>
                            <th>First Flight</th>
                        </tr>
                        {% for rocket in rockets %}
                        <tr>
                            <td>{{ rocket.id }}</td>
                            <td>{{ rocket.name }}</td>
                            <td>{{ rocket.success_rate_pct }}</td>
                            <td>{{ rocket.cost_per_launch }}</td>
                            <td>{{ rocket.height_meters }}</td>
                            <td>{{ rocket.diameter_meters }}</td>
                            <td>{{ rocket.mass_kg }}</td>
                            <td>{{ rocket.thrust_sea_level_kN }}</td>
                            <td>{{ rocket.thrust_vacuum_kN }}</td>
                            <td>{{ rocket.first_flight }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </body>
                </html>
            """, rockets=rockets)
        # Give the data in JSON format
        elif response_type is None or response_type == 'json':
            logger.info("Returning data of rockets in JSON format.")
            return jsonify([rocket.to_dict() for rocket in rockets])
    except ValueError as v:
        logger.error(f"ValueError in /rockets endpoint: {v}")
        return jsonify({"error": str(v)}), 400
    except Exception as e:
        logger.error(f"Error in /rockets endpoint: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@api.route('/launches', methods=['GET'])
@api.route('/launches/<response_type>', methods=['GET'])
def get_clear_launches(response_type=None):
    """
    Endpoint to get launches data with optional filtering and sorting.

    Args:
    response_type (string, optional (JSON or HTML)): Response type ('html' or 'json'). If not specified, returns JSON.

    Returns:
    JSON or HTML: Rocket data in the specified format.
    
    Examples of querys:
    
    api/launches?filter_field=date_utc&filter_value=2022&sort_low=flight_number
    
    api/launches/json?filter_field=date_utc&filter_value=2020-05-24&sort_high=success
    
    api/launches/hmtl?sort_high=date_utc

    Query format:
    
    api/launches?filter_field={filter_field}&filter_value={possible_filter_value}&sort_low={sort_high / sort_low}
    
    api/launches/{format}?filter_field={filter_field}&filter_value={possible_filter_value}&sort_low={sort_high / sort_low}
    
    Can sort any value except id and can filter any value.
    
    The format is json or html.
    """
    session = Session()
    logger.info("Accessed /launches-clear endpoint")
    try:
        # Get sorting and filtering parameters from the request
        sort_param = request.args.get('sort_high') or request.args.get('sort_low')
        sort_order = 'desc' if request.args.get('sort_high') else 'asc'
        filter_field = request.args.get('filter_field')
        filter_value = request.args.get('filter_value')
        
        # Validate that both filtering parameters are present
        if (filter_field and not filter_value) or (not filter_field and filter_value):
            logger.error("Both filter_field and filter_value must be provided for filtering.")
            return jsonify({"error": "Both filter_field and filter_value must be provided for filtering."}), 400
        
        # Get launches data by applying filtering and sorting if specified
        launches = get_filter_sort_launches(session, sort_param, sort_order, filter_field, filter_value)
        
        # In case launches with the filtering specifications are not found
        if not launches:
            logger.error("No launches found matching the specifications")
            return jsonify({"message": "No launches found matching the specifications"}), 404
        
        logger.info("Getting the processed data of launches")
        
        # Give the data in a HTML table format
        if response_type == 'html':
            logger.info("Returning data of launches in HTML format")
            return render_template_string("""
                <html>
                <head>
                    <style>
                        table, h1 {
                            border-collapse: collapse;
                            width: 80%;
                            margin: auto;
                            text-align: center;
                        }
                        th, td {
                            padding: 8px;
                            border: 1px solid black;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                    </style>
                </head>
                <body>
                    <h1>Launches</h1> <!-- Table title -->
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Date UTC</th>
                            <th>Success</th>
                            <th>Rocket ID</th>
                            <th>Flight Number</th>
                        </tr>
                        {% for launch in launches %}
                        <tr>
                            <td>{{ launch.id }}</td>
                            <td>{{ launch.name }}</td>
                            <td>{{ launch.date_utc }}</td>
                            <td>{{ launch.success }}</td>
                            <td>{{ launch.rocket_id }}</td>
                            <td>{{ launch.flight_number }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </body>
                </html>
            """, launches=launches)
        # Give the data in JSON format
        elif response_type is None or response_type == 'json':
            logger.info("Returning data of launches in JSON format")
            return jsonify([launch.to_dict() for launch in launches])
    except ValueError as v:
        logger.error(f"ValueError in /launches endpoint: {v}")
        return jsonify({"error": str(v)}), 400
    except Exception as e:
        logger.error(f"Error in /launches endpoint: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@api.route('/starlink', methods=['GET'])
@api.route('/starlink/<response_type>', methods=['GET'])
def get_clear_starlink(response_type=None):
    """
    Endpoint to get starlink data with optional filtering and sorting.

    Args:
    response_type (string, optional (JSON or HTML)): Response type ('html' or 'json'). If not specified, returns JSON.

    Returns:
    JSON or HTML: Rocket data in the specified format.
    
    Examples of querys:
    
    api/starlink?filter_field=launch_date&filter_value=2022&sort_low=inclination
    
    api/starlink/json?filter_field=launch_date&filter_value=2020-02-17&sort_high=periapsis
    
    api/starlink/html?sort_low=mass_kg

    Query format:
    
    api/starlink?filter_field={filter_field}&filter_value={possible_filter_value}&sort_low={sort_high / sort_low}
    
    api/starlink/{format}?filter_field={filter_field}&filter_value={possible_filter_value}&sort_low={sort_high / sort_low}
    
    Can sort any value except id and can filter any value.
    
    The format is json or html.
    """
    session = Session()
    logger.info("Accessed /starlink-clear endpoint")
    try:
        # Get sorting and filtering parameters from the request
        sort_param = request.args.get('sort_high') or request.args.get('sort_low')
        sort_order = 'desc' if request.args.get('sort_high') else 'asc'
        filter_field = request.args.get('filter_field')
        filter_value = request.args.get('filter_value')
        
        # Validate that both filtering parameters are present
        if (filter_field and not filter_value) or (not filter_field and filter_value):
            logger.error("Both filter_field and filter_value must be provided for filtering.")
            return jsonify({"error": "Both filter_field and filter_value must be provided for filtering."}), 400
        
        # Get rocket data by applying filtering and sorting if specified
        starlinks = get_filter_sort_starlink(session, sort_param, sort_order, filter_field, filter_value)
        
        # In case rockets with the filtering specifications are not found
        if not starlinks:
            logger.error("No starlinks found matching the specifications")
            return jsonify({"message": "No starlinks found matching the specifications"}), 404
        
        logger.info("Getting the processed data of rockets")
        
        # Give the data in a HTML table format
        if response_type == 'html':
            logger.info("Returning data of starlink in HTML format")
            return render_template_string("""
                <html>
                <head>
                    <style>
                        table, h1 {
                            border-collapse: collapse;
                            width: 80%;
                            margin: auto;
                            text-align: center;
                        }
                        th, td {
                            padding: 8px;
                            border: 1px solid black;
                        }
                        th {
                            background-color: #f2f2f2;
                        }
                    </style>
                </head>
                <body>
                    <h1>Launches</h1> <!-- Table title -->
                    <table>
                        <tr>
                            <th>ID</th>
                            <th>Object Name</th>
                            <th>Launch Date</th>
                            <th>Decay Date</th>
                            <th>Inclination</th>
                            <th>Apoapsis</th>
                            <th>Periapsis</th>
                            <th>Launch ID</th>
                        </tr>
                        {% for s in starlink %}
                        <tr>
                            <td>{{ s.id }}</td>
                            <td>{{ s.object_name }}</td>
                            <td>{{ s.launch_date }}</td>
                            <td>{{ s.decay_date }}</td>
                            <td>{{ s.inclination }}</td>
                            <td>{{ s.apoapsis }}</td>
                            <td>{{ s.periapsis }}</td>
                            <td>{{ s.launch_id }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </body>
                </html>
            """, starlink=starlinks)
        # Give the data in JSON format
        elif response_type is None or response_type == 'json':
            logger.info("Returning data of starlink in JSON format")
            return jsonify([s.to_dict() for s in starlinks])
    except ValueError as ve:
        logger.error(f"ValueError in /starlink endpoint: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error in /starlink endpoint: {e}")
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

@api.route('test_error', methods=["GET"])
def test_error_501():
    """
    Endpoint to get the dashboard with statistics.
    """
    logger.info("Accessed /test_error endpoint")
    logger.critical("Endpoint /api/.. doesn't exist yet.")
    return {"message": "Dashboard endpoint not yet implemented"}, 501