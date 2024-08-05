from flask import Flask, jsonify, Blueprint, make_response, request, render_template_string
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Internal classes.
from config import DATABASE_URI
from constants import LAUNCHES
from helpers.logger import logger
from backend.spaceX.spaceX_data import get_data
from backend.launches_resources.launches_filter_sort import get_filter_sort_launches
from backend.api import api

# Create the database engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

launches_bp = Blueprint(LAUNCHES, __name__)

@api.route('/launches-raw', methods=["GET"])
def get_launches():
    """
    Function to get all the launches
    """
    logger.info("Accessed /launches endpoint")
    try:
        data, status_code = get_data(LAUNCHES)
        logger.info(make_response(jsonify(data),status_code))
        return data, status_code
    except Exception as e:
        logger.error(f"Error in /launches endpoint: {e}")
        return jsonify({"error": str(e)}), 500

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