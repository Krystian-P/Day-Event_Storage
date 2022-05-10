from flask import Flask
from app import model
from config import Config

# Initialize application
app = Flask(__name__)
app.config.from_object(Config)

# Initialize connection with database
model.dataBase.initialize()

from app import routes, model


