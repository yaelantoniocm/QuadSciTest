from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database URI from environment variables
DATABASE_URI = os.getenv('DATABASE_URI')