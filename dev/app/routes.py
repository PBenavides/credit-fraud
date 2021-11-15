import time
from flask import render_template, request, jsonify
from app import app
from app.pipeline import InferencePipeline #For Data Pipeline
from app.utils import validate_dict  #For Validation

@app.route('/')
def index():
    message='Hi, Welcome to the API'
    return render_template('index.html', message=message)

@app.route('/predict', methods=['GET','POST'])
def predict():
    
    if request.method == 'GET':
        return render_template('predict.html')

    elif request.method == 'POST':

        start = time.time()
        
        data = request.json
        
        print('Received request data')
        print('As type', type(data))
        
        #DATA VALIDATION

        validation = validate_dict(data)
        if validation != 'pass':
            return jsonify({'message': validation})

        #PREDICTION
        pred = InferencePipeline(data_dict=data).predict()
        
        print('Success validation')
        end = time.time()

        print(end-start)
        return jsonify({'message': 'Success',
                    'prediction_class': pred
        })

    return jsonify({'message':'METHOD NOT FOUND'})