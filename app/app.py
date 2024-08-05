from flask import Flask
from threading import Thread

from backend.application.api import api
from backend.storage import start_scheduler
from databases.models import create_tables

from config import DATABASE_URI

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI 
    app.register_blueprint(api, url_prefix='/api')
    return app

app = create_app()

with app.app_context():
    # Create the database tables if they do not exist
    create_tables()
    
    # Start the scheduler within the context of the application, this to run in a parallel thread
    scheduler_thread = Thread(target=start_scheduler, args=(app,))
    scheduler_thread.start()

if __name__ == "__main__":
    app.run(debug=True, port=5001)