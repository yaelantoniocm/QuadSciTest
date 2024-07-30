# Dependencies
from flask import Flask, jsonify, Blueprint
import requests

api = Blueprint('api', __name__)


# The API Requets URL for "SpaceX API"
API_requests = "https://api.spacexdata.com/v4/" 


def get_data(endpoint: str) -> dict:
    """
    Function to get data from the API
    """
    url = f"{API_requests}{endpoint}"
    response = requests.get(url)
    return response.json()

@api.route('dashboard', methods=["GET"])
def get_dashboard():
    """
    Function to get the dashboards
    """
    pass

@api.route('rockets', methods=["GET"])
def get_rockets():
    """
    Function to get all rockets
    """
    return get_data("rockets")
    
@api.route('launches', methods=["GET"])
def get_launches():
    """
    Function to get all the launches
    """
    return get_data("launches")

