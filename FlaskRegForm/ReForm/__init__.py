from flask import Flask
from config import Config

ReForm = Flask(__name__)
ReForm.config.from_object(Config)

from ReForm import routes