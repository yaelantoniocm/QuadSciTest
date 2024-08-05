# Dependencies
from flask import Flask, jsonify, Blueprint, make_response, request, render_template_string
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Internal classes
from helpers.logger import logger
from backend.spaceX.spaceX_data import get_data
from backend.starlink_resources.starlink_filter_sort import get_filter_sort_starlink
from constants import STARLINK
from config import DATABASE_URI

# Create the database engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

starlink_bp = Blueprint(STARLINK, __name__)

@starlink_bp.route('-raw', methods=["GET"])
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

@starlink_bp.route('', methods=['GET'])
@starlink_bp.route('/<response_type>', methods=['GET'])
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