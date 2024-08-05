# Dependencies
from flask import Flask, jsonify, Blueprint, make_response, request, render_template_string
import requests

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Other classes
from helpers.logger import logger
from config import DATABASE_URI
from constants import API_PREFIX

# Importa y registra cada Blueprint
from backend.rocket_resources.rockets import rockets_bp
from backend.launches_resources.launches import launches_bp
from backend.starlink_resources.starlink import starlink_bp

# Create the database engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

api = Blueprint('api', __name__)

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

# Register each Blueprint under the API_PREFIX
api.register_blueprint(rockets_bp)
api.register_blueprint(launches_bp)
api.register_blueprint(starlink_bp)