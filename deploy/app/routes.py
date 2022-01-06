import time
import logging
from flask import render_template, request, jsonify
from app import app
from app.pipeline import InferencePipeline #For Data Pipeline
from app.utils import validate_dict, InvalidDataError  #For Validation

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    message='Hi, Welcome to the Credit-Fraud Detection API'
    return render_template('index.html', message=message)

@app.route('/predict', methods=['GET','POST'])
def predict():
    
    if request.method == 'GET':
        return render_template('predict.html')

    elif request.method == 'POST':

        start = time.time() #To log time to prediction
        
        data = request.json

        logger.debug('Received request data as type {}'.format(type(data)))

        #DATA VALIDATION
        try: 
            validate_dict(data)

        except InvalidDataError as e:
            return jsonify({'message': e.message}), 400

        #PREDICTION
        data_pipeline = InferencePipeline(data_dict = data)  #Apply the pipeline to the data
        
        prediction = data_pipeline.predict(model_name='ET')  #Make inference with model you like

        logger.debug('Success prediction of:{}'.format(prediction))
        
        end = time.time()
        logger.debug('Pipeline time:{}'.format(str(end-start)))

        return jsonify({'message': 'Success',
                    'prediction_class': prediction
        }), 200

    return jsonify({'message':'METHOD NOT FOUND'})