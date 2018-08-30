from keras.models import model_from_json
import tensorflow as tf
import json
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np

"""
@params : Nothing
@return : loaded_model, graph(Tensors)
what it does : it loads the models within it's graph
"""
def init_cnn():
	# load the json_format of the model
	json_file = open('models/avito_model.json','r')
	loaded_model_json = json_file.read()
	json_file.close()

	#load woeights into new model
	loaded_model = model_from_json(loaded_model_json)
	loaded_model.load_weights("models/avito_model.h5")

	#compile and evaluate loaded model
	loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

	graph = tf.get_default_graph()

	return loaded_model, graph


"""
@params : image, target (matrix, tuple)
@return : image (matrix)
what it does : resize the given image to the appropriate size
"""
def preprocess_image(image,target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image,axis = 0)
    return image