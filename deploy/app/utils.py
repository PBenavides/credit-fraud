import pickle
import os
import datetime
import numpy as np
import logging
from schema import Schema, SchemaError

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ARTIFACT_DIR = os.path.join(BASE_DIR, 'artifacts')

def load_artifacts():
    """Load artifacts dictionary
    """
    
    artifacts_list = ['ET','LDA','XGB','voting_final','normalizer']

    artifacts_dict = dict()
    
    for artifact_name in artifacts_list:

        with open(os.path.join(ARTIFACT_DIR, artifact_name + '.sav'), 'rb') as handle:
            artifact = pickle.load(handle)
            artifacts_dict[artifact_name] = artifact

    return artifacts_dict

class InvalidDataError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def validate_dict(data):
    """
    To validate POST request.
    """
    #Schema data-structure
    schema_dict_sample = {f"V{i}": float for i in range(1,29)}
    schema_dict_sample["Amount"] = float

    #Build Schema
    schema = Schema(
        schema_dict_sample, ignore_extra_keys=True
    )

    #Validation Handler
    try:
        schema.validate(data)
        return 'pass'

    except SchemaError as err:
        logging.debug('ERROR:{}'.format(err.__dict__['autos'][-1]))
        raise InvalidDataError("Something failed: {}".format(
            err.__dict__['autos'][-1]))

def get_time_now():
    """Just like the dataset, get time in seconds
    counting from midnight UTC
    """
    today_utc = datetime.datetime.utcnow()

    hour = today_utc.hour * 3600

    minutes = today_utc.minute * 60

    total_seconds = hour + minutes + today_utc.second

    return total_seconds

def get_time_sin_cos(seconds):
    """Get time transformen in sin-cos cyclical values
    seconds: #of seconds in day
    """

    SECONDS_PER_DAY = 60*60*24

    sin_time = np.sin(2*np.pi*seconds/SECONDS_PER_DAY)
    cos_time = np.cos(2*np.pi*seconds/SECONDS_PER_DAY)  

    return sin_time, cos_time