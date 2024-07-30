import logging
import os
from datetime import datetime


def log_messages():
    # Get the current dirtectory 
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Go up one level to get the project root directory
    project_root = os.path.abspath(os.path.join(current_directory, '..'))
    
    # We create the folder log if doesn't exists
    log_dir = log_dir = os.path.join(project_root, 'log')
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # We generate the log file with the date (dd/mm/year_hour-minutes) to be to be unique log files
    log_filename = os.path.join(log_dir, 'log-' +  (datetime.now().strftime('%d-%m-%Y_%H-%M')) + '.log')

    # Configuration of the logger
    logger = logging.getLogger("SpaceX-API")
    logger.setLevel(logging.DEBUG)

    """
    Create the handler to write the log file.
    By not defining the logging level it inherits it from logger (logger is the parent)
    """
    file_handler = logging.FileHandler(log_filename)

    # Giving the format of the message and adding to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)
    
    return logger