from flask import Flask, render_template, request, jsonify
from helper import *
from werkzeug import secure_filename
import os

# set the upload folder
UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

# load the LSTM model we've trained before
global cnn_model, cnn_graph
cnn_model, cnn_graph = init_cnn()

# home page
@app.route('/')
def home():
   return render_template('index.html')


# procesing uploaded file and predict it
@app.route('/upload', methods=['POST','GET'])
def upload_file():

	if request.method == 'GET':
	    return render_template('index.html')
	else:
		ad_category = int(request.form['ad_category'])
		print('ad_category is',ad_category)
		file = request.files['image']
		full_name = os.path.join(UPLOAD_FOLDER, file.filename)
		file.save(full_name)

		classes = {0: 'laptop', 1: 'phone'}

		#read the saved image from uploads directory 
		img = Image.open(UPLOAD_FOLDER+'/'+file.filename)

		processed_image = preprocess_image(img,target_size = (64, 64))

		matrix = []
		matrix.append(processed_image)
		# it's time to predict what's on that image
		with cnn_graph.as_default():
			prediction = cnn_model.predict(matrix).tolist()

		# get the prediction signle value
		prediction = np.asscalar(np.argmax(prediction, axis=1))
		are_matched = True if prediction == ad_category else False

		if prediction == 0:
		    return jsonify({'class' : classes[0], 'categories_matched': are_matched})
		else:
		    return jsonify({'class' : classes[1], 'categories_matched': are_matched})



if __name__ == '__main__':
    app.run(debug=True)
