from flask import Flask
# from flask.cli import load_dotenv
from dotenv import load_dotenv
import os

from routes.routes import configure_routes

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
