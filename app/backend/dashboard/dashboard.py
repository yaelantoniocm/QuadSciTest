# Dependencies
from app.helpers.statistics import get_launch_statistics, get_rocket_statistics, get_starlink_statistics
from flask import Flask, jsonify, Blueprint, render_template_string
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Internal classes
from helpers import logger
from constants import DASHBOARD
from config import DATABASE_URI

# Create the database engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

dashboard_bp = Blueprint(DASHBOARD, __name__)

@dashboard_bp.route('/dashboard', methods=["GET"])
@dashboard_bp.route('/dashboard/<response_type>', methods=['GET'])
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