import pickle
import os
import datetime
import numpy as np

from schema import Schema, SchemaError

def load_artifacts():
    """Load artifacts dictionary
    """
    dir = os.getcwd()
    with open(dir+'\\app\\artifacts\\tuned_et.sav','rb') as handle:
        et_model = pickle.load(handle)

    with open(dir+'\\app\\artifacts\\LDA.sav','rb') as handle:
        lda_model = pickle.load(handle)

    with open(dir+'\\app\\artifacts\\first_xgb.sav','rb') as handle:
        xgb_model = pickle.load(handle)

    with open(dir+'\\app\\artifacts\\voting_final.sav','rb') as handle:
        voting_model = pickle.load(handle)

    with open(dir+'\\app\\artifacts\\normalizer.sav','rb') as handle:
        normalizer = pickle.load(handle)

    artifacts_dict = {
        'normalizer' : normalizer,
        'et_model' : et_model,
        'lda_model': lda_model,
        'xgb_model': xgb_model,
        'voting_model': voting_model,
    }

    return artifacts_dict

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

    #Handle Validation
    try:
        schema.validate(data)
        return 'pass'

    except SchemaError as err:
        error_str = repr(err.__dict__['autos'][-1])
        print(error_str)
        return error_str
    
