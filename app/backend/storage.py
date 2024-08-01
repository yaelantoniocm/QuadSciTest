import os
import json
from flask import current_app, Flask

# Extra imports
from datetime import datetime  
from apscheduler.schedulers.background import BackgroundScheduler

# Functions from other files
from backend.api import get_rockets, get_launches, get_starlink
from helpers.logger import logger

def save_data(app):
    """
    Function to save the data of the API calls from Space X, we will save it in JSON 
    and move old files to the backup folder.
    """
    with app.app_context():
        logger.info("Starting the save_data process")
        
        # Define the endpoints
        endpoints = {
            "rockets": get_rockets,
            "launches": get_launches,
            "starlink": get_starlink
        }
        
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
        # Soret the files with the modification time
        files.sort(key=lambda f: os.path.getmtime(os.path.join(data_subdir, i))) 
    
    
    # All files are moved to the backup folder except the most recent one.
        for file in files[:-1]:
            source = os.path.join(data_subdir, file)
            destination = os.path.join(backup_subdir, file)
            # os.rename: this function move o rename, if there are in the same path, the funtion rename the file, else, move
            os.rename(source, destination)
            logger.info(f"Moved {source} to {destination}")  
    else:
        logger.info(f"No older files to move to backup in {data_subdir}") 

def start_scheduler(app):
    """
    Start the scheduler and execute the save_data method immediately.
    """
        
    # Schedule the save_data function to run every 12 hours.
    scheduler = BackgroundScheduler()
    #scheduler.add_job(save_data, 'interval', hours=12)
    # logger.info("Scheduler started to every 1 minute")
    scheduler.add_job(save_data, 'interval', seconds=60, args=[app])
    logger.info("Scheduler started to every 1 minute")
    scheduler.start()