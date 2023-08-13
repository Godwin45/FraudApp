from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from mlProject.pipeline.prediction import PredictionPipeline


app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")


@app.route('/train',methods=['GET'])  # route to train the pipeline
def training():
    os.system("python main.py")
    return "Training Successful!" 


@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            # Reading the inputs given by the user
            scaled_amount = float(request.form['scaled_amount'])
            scaled_time = float(request.form['scaled_time'])
            V1 = float(request.form['V1'])
            V2 = float(request.form['V2'])
            V3 = float(request.form['V3'])
            V4 = float(request.form['V4'])
            V5 = float(request.form['V5'])
            V6 = float(request.form['V6'])
            V7 = float(request.form['V7'])
            V8 = float(request.form['V8'])
            V9 = float(request.form['V9'])
            V10 = float(request.form['V10'])
            V11 = float(request.form['V11'])
            V12 = float(request.form['V12'])
            V13 = float(request.form['V13'])
            V14 = float(request.form['V14'])
            V15 = float(request.form['V15'])
            V16 = float(request.form['V16'])
            V17 = float(request.form['V17'])
            V18 = float(request.form['V18'])
            V19 = float(request.form['V19'])
            V20 = float(request.form['V20'])
            V21 = float(request.form['V21'])
            V22 = float(request.form['V22'])
            V23 = float(request.form['V23'])
            V24 = float(request.form['V24'])
            V25 = float(request.form['V25'])
            V26 = float(request.form['V26'])
            V27 = float(request.form['V27'])
            V28 = float(request.form['V28'])
            
            data = [
                scaled_amount, scaled_time, V1, V2, V3, V4, V5, V6, V7, V8, V9, V10,
                V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24,
                V25, V26, V27, V28
            ]
            
            data = np.array(data).reshape(1, 30)
            
            obj = PredictionPipeline()
            predict = obj.predict(data)

            return render_template('results.html', prediction = str(predict))

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'

    else:
        return render_template('index.html')


if __name__ == "__main__":
	# app.run(host="0.0.0.0", port = 8080, debug=True)
	app.run(host="0.0.0.0", port = 8080)