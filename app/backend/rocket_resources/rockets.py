# Dependencies

from flask import Flask, jsonify, Blueprint, make_response, request, render_template_string
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Internal classes
from helpers.logger import logger
from backend.spaceX.spaceX_data import get_data
from backend.rocket_resources.rocket_filter_sort import get_filter_sort_rocket
from constants import ROCKETS
from config import DATABASE_URI

# Import the Blueprint from api.py
from backend.api import api

# Create the database engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

@api.route('/rockets-raw', methods=["GET"])
def get_rockets():
    """
    Function to get all rockets and the status code(200,300,400,500)

    Returns:
        GET: Return all the data of rockets in JSON format 
    """
    logger.info("Accessed /rockets endpoint")
    try:
        data, status_code = get_data(ROCKETS)
        logger.info(make_response(jsonify(data),status_code))
        return data, status_code
    except Exception as e:
        logger.error(f"Error in /rockets endpoint: {e}")
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