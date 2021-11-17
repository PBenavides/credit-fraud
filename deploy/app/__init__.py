import logging

from flask import Flask
from config import Config
from app.utils import load_artifacts


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(message)s"
)

app = Flask(__name__)
app.config.from_object(Config)

artifacts_dict = load_artifacts()  #LOAD ARTIFACTS

from app import routes, utils, pipeline