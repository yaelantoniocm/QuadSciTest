from datetime import datetime  
from flask import current_app, Flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

from models import Rockets, Launches, Starlink, Base
from config import DATABASE_URI

import os
import json
import time

# Functions from other files
from backend.api import get_rockets, get_launches, get_starlink
from helpers.logger import logger

def save_data(app):
    """
    Function to save the data of the API calls from Space X, we will save it in JSON 
    and move old files to the backup folder.
    
    Args:
        app (Flask): Flask application context.
    """
    with app.app_context():
        logger.info("Starting the save_data process")
        
        # Define the endpoints
        endpoints = {
            "rockets": get_rockets,
            "launches": get_launches,
            "starlink": get_starlink
        }
        
        # Dictionary to store all data
        all_data = {}  
        
        # Get the base directory for this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define the destination directories (for data and for backup)
        data_dir = os.path.join(base_dir, '..', 'data')
        backup_dir = os.path.join(base_dir, '..', 'backup')
        
        for key, func in endpoints.items():
            # Get the current timestamp in the specified format. 
            time_stamp = datetime.now().strftime('%d-%m-%Y_%H-%M')
            
            # Create the directory for the data (rockets, launches, starlink) and the backup if doesn't exist
            data_subdir = os.path.join(data_dir , key)
            backup_subdir = os.path.join(backup_dir, key)
            
            os.makedirs(data_subdir, exist_ok=True)
            os.makedirs(backup_subdir, exist_ok=True)
            
            # Get the data of the APIs calls
            data, status_code = func()
            
            if status_code == 200:
                # Save the data in a new JSON file.
                file_name = f"raw-{key}-{time_stamp}.json"
                file_path = os.path.join(data_subdir, file_name)
                
                with open(file_path, 'w') as json_file:
                    json.dump(data, json_file, indent= 4)
                    logger.info(f"The data was successfully saved to {file_path}")
                move_to_backup(data_subdir, backup_subdir)
            else:
                logger.error(f"Failed to fetch data for {key}")
    
        # Start a thread to run save_to_db after we save the JSON and move the JSON to the backup.
        db_thread = Thread(target=save_to_db, args=(data_dir,))
        db_thread.start()
            
def move_to_backup(data_subdir, backup_subdir):
    """
    Function to move the old JSON files (data of rockets, or launches or starlink to the backup Folder)
    Args:
        data_subdir (path): The subdirectory where the data is saved (Ex: data/rockets)
        backup_subdir (path): The subdirectory where the old data will be save (Ex: backup/rockets)
    """
    
    files = []  

    # Iterate over each file in the directory, check if the file ends with '.json', if so, add it to the 'files' list
    for i in os.listdir(data_subdir): 
        if i.endswith('.json'):  
            files.append(i)  
    
    # Sort all the JSON by modification date if there is more than 1
    if len(files) > 1:
        # Sorted the files with the modification time
        files.sort(key=lambda f: os.path.getmtime(os.path.join(data_subdir, f))) 
    
    
    # All files are moved to the backup folder except the most recent one.
        for file in files[:-1]:
            source = os.path.join(data_subdir, file)
            destination = os.path.join(backup_subdir, file)
            # os.rename: this function move o rename, if there are in the same path, the funtion rename the file, else, move
            os.rename(source, destination)
            logger.info(f"Moved {source} to {destination}")  
    else:
        logger.info(f"No older files to move to backup in {data_subdir}") 
    
    # Ensure only the 40 most recent files are kept in the backup folder
    cleanup_backup_folder(backup_subdir)

def cleanup_backup_folder(backup_subdir):
    """
    Function to clean up the backup folder, ensuring only the 40 most recent files are kept.
    Args:
        backup_subdir (path): The subdirectory where the backup data is saved (backup/rockets)
    """
    files= []
    # Iterate over each file in the backup directory, check if the file ends with '.json', if so, add it to the 'files' list
    for i in os.listdir(backup_subdir):
        if i.endswith('.json'):
            files.append(i)
    
    # Sort all the JSON files by modification date
    if len(files) > 40:
        # Sort the files by modification time
        files.sort(key=lambda f: os.path.getmtime(os.path.join(backup_subdir, f)))

        # Remove the oldest files, keeping only the 40 most recent
        files_to_remove = files[:-40]
        for file in files_to_remove:
            os.remove(os.path.join(backup_subdir, file))
            logger.info(f"Removed old backup file: {file}")

def save_to_db(data_dir):
    """Save the transformed data to the SQL database.

    Args:
        data (list): List of data items to be saved.
        data_type (string): The type of data being saved (e.g., 'rockets', 'launches', 'starlink').
    """
    try:
        # Create the database engine and session
        engine = create_engine(DATABASE_URI)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        
        # Load and save rockets data
        rockets_dir = os.path.join(data_dir, 'rockets')
        # To save the rockets data.
        if os.path.exists(rockets_dir):
            for file in os.listdir(rockets_dir):
                if file.endswith('.json'):
                    with open(os.path.join(rockets_dir, file), 'r') as json_file:
                        data = json.load(json_file)
                        for item in data:
                            rocket = Rockets(
                                id=item['id'],
                                name=item['name'],
                                success_rate_pct=item['success_rate_pct'],
                                cost_per_launch=item['cost_per_launch'],
                                height_meters=item['height']['meters'],
                                diameter_meters=item['diameter']['meters'],
                                mass_kg=item['mass']['kg'],
                                thrust_sea_level_kN=item['first_stage']['thrust_sea_level']['kN'],
                                thrust_vacuum_kN=item['first_stage']['thrust_vacuum']['kN'],
                                first_flight=item['first_flight']
                            )
                            session.merge(rocket)
            logger.info("Rocket data saved to the database.")
        else:
            logger.error("Rocket information is empty.")
        
        # Load and save launches data
        launches_dir = os.path.join(data_dir, 'launches')
        if os.path.exists(launches_dir):
            for file in os.listdir(launches_dir):
                if file.endswith('.json'):
                    with open(os.path.join(launches_dir, file), 'r') as json_file:
                        data = json.load(json_file)
                        for item in data:
                            launch = Launches(
                                id=item['id'],
                                name=item['name'],
                                date_utc=item['date_utc'],
                                success=item['success'],
                                rocket_id=item['rocket'],
                                flight_number=item['flight_number'],
                            )
                            session.merge(launch)
            logger.info("Launch data saved to the database.")
        else:
            logger.error("Launches information is empty.")
        
        # Load and save starlink data
        starlink_dir = os.path.join(data_dir, 'starlink')
        if os.path.exists(starlink_dir):
            for file in os.listdir(starlink_dir):
                if file.endswith('.json'):
                    with open(os.path.join(starlink_dir, file), 'r') as json_file:
                        data = json.load(json_file)
                        for item in data:
                            starlink = Starlink(
                                id=item['id'],
                                object_name=item['spaceTrack']['OBJECT_NAME'],
                                launch_date=item['spaceTrack']['LAUNCH_DATE'],
                                decay_date=item['spaceTrack']['DECAY_DATE'],
                                inclination=item['spaceTrack']['INCLINATION'],
                                apoapsis=item['spaceTrack']['APOAPSIS'],
                                periapsis=item['spaceTrack']['PERIAPSIS'],
                                launch_id=item['launch']
                            )
                            session.merge(starlink)
            logger.info("Starlink data saved to the database.")
        else:
            logger.error("Starlink information is empty.")
        session.commit()
        
    except Exception as e:
        logger.error(f"Error saving data to the database: {e}")
    finally:
        session.close()

def start_scheduler(app):
    """
    Start the scheduler and execute the save_data method immediately.
    """
        
    # Schedule the save_data function to run every 12 hours.
    scheduler = BackgroundScheduler()
    #scheduler.add_job(save_data, 'interval', hours=12)
    # logger.info("Scheduler started to every 1 minute")
    scheduler.add_job(save_data, 'interval', seconds=80, args=[app])
    logger.info("Scheduler started to every 1 minute")
    scheduler.start()