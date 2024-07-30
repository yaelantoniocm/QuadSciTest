from flask import Flask
from api import api
import sys
import os

# Agregar la ruta del directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
