from flask import Flask,jsonify,request
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import flasgger
from flasgger import Swagger
import joblib
import pickle

app=Flask(__name__)
Swagger(app)


@app.route('/')
def index():
	return 'Welcome All'

@app.route('/train')
def train():
	df_train = pd.read_excel('False Alarm Cases.xlsx')
	df_train = df_train.iloc[:, 1:8]
	X = df_train.iloc[:,0:6]
	y = df_train['Spuriosity Index(0/1)']
	
	classifier = GaussianNB()
	classifier.fit(X, y)
	joblib.dump(classifier, 'filename.pkl')
	return 'Model has been Trained'
	
@app.route('/test', methods=['POST'])
def test():
	"""Let's Check alarm  
	    This is using docstrings for specifications.
	    ---
	    parameters:  
	      - name: Ambient Temperature
	        in: query
	        type: number
	        required: true
	      - name: Calibration
	        in: query
	        type: number
	        required: true
	      - name: Unwanted substance deposition
	        in: query
	        type: number
	        required: true
	      - name: Humidity
	        in: query
	        type: number
	        required: true
	      - name: H2S Content
	        in: query
	        type: number
	        required: true
	      - name: detected by
	        in: query
	        type: number
	        required: true  
	    responses:
	        200:
	            description: The output values

	    """
	clf = joblib.load('filename.pkl')
	a = request.args.get("Ambient Temperature")
	b = request.args.get("Calibration")
	c = request.args.get("Unwanted substance deposition")
	d = request.args.get("Humidity")
	e = request.args.get("H2S Content")
	f = request.args.get("detected by")
	l = [a, b, c, d, e, f]
	narr = np.array(l)
	narr = narr.reshape(1, 6)
	df_test = pd.DataFrame(narr, columns=['Ambient Temperature', 'Calibration', 'Unwanted substance deposition',
										  'Humidity', 'H2S Content', 'detected by'])

	prediction = clf.predict(df_test)
	print(prediction)
	if prediction == 1:
		result = 'Danger'

	else:
		result = 'No Danger'


	return "Hello The answer is " + str(result)
	#return str(list(prediction))
	

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
