from flask import Flask
from threading import Thread

from backend.api import api
from backend.storage import start_scheduler
from helpers.logger import logger

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/api')
    return app

app = create_app()

with app.app_context():
    # Start the scheduler within the context of the application, this to run in a parallel thread
    scheduler_thread = Thread(target=start_scheduler, args=(app,))
    scheduler_thread.start()

if __name__ == "__main__":
    app.run(debug=True, port=5001)