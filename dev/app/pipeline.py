import pandas as pd
import datetime
import numpy as np
import json

from app import artifacts_dict as artifacts
from app.utils import get_time_now, get_time_sin_cos

class InferencePipeline():
    """Pipeline to receive data_dict and transform for inference.
    ---------
    Parameters:
    data_dict:
    
    """
    def __init__(self, data_dict):

        self.data = data_dict
        self.time = datetime.datetime.utcnow
        
    def create_features(self):
        """Adds features to data
        """
        seconds = get_time_now()
        sin_time, cos_time = get_time_sin_cos(seconds)

        self.data['sin_time'] = sin_time
        self.data['cos_time'] = cos_time


    def normalize_columns(self):
        """Normalize data
        --------
        output: pd.DataFrame object
        """

        self.normalizer = artifacts['normalizer']

        to_norm = pd.DataFrame(data={0: self.data}).T.infer_objects()

        self.transformed_data = self.normalizer.transform(to_norm.values)

        X_norm = pd.DataFrame(self.transformed_data, index=[0], #index = [0] to have one inf in pandas
                columns= to_norm.columns
                ) 
        
        return X_norm


    def transform_to_infer(self):
        """Transform data. Ready to predict
        """
        self.create_features()

        X = self.normalize_columns()

        return X

    def predict(self):
        """Predict from data request
        """

        X = self.transform_to_infer()
        model_one = artifacts['voting_model']
        prediction = model_one.predict(X)

        pred_json = json.dumps(prediction.tolist())

        return pred_json