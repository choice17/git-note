# FLASK KERAS RESTFUL API

## reference  

[link](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html)

## installation  

`$ pip install flask gevent requests pillow`

## building script

* build_keras_api  

```python
"""run_keras_server.py"""
# import the necessary packages
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io

app = flask.Flask(__name__)
model = None
```

* With load model functions.

```python
def load_model():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    global model
    model = ResNet50(weights="imagenet")
```

* Input preprocessing.

```python
def prepare_image(image, target):
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image
```

* RESTFUL service. POST command allows sending arbitrary data.

```python
@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            # preprocess the image and prepare it for classification
            image = prepare_image(image, target=(224, 224))

            # classify the input image and then initialize the list
            # of predictions to return to the client
            preds = model.predict(image)
            results = imagenet_utils.decode_predictions(preds)
            data["predictions"] = []

            # loop over the results and add them to the list of
            # returned predictions
            for (imagenetID, label, prob) in results[0]:
                r = {"label": label, "probability": float(prob)}
                data["predictions"].append(r)

            # indicate that the request was a success
            data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)
```

* Start up script

```python
if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    app.run()
```


## Client

```python
# import the necessary packages
import requests
import argparse

# initialize the Keras REST API endpoint URL along with the input
# image path
KERAS_REST_API_URL = "http://localhost:5000/predict"
IMAGE_DIR = 'dog.jpg'


def getparse():
	parser = argparse.ArgumentPaser()
	parser.add_argument('-i', type=str, default=IMAGE_DIR, help='input image dir')
	parser.add_argument('-u', type=str, default=KERAS_REST_API_URL, help='rest service ip')
	return parser.parse_args()

# load the input image and construct the payload for the request
def POST(args):
	image = open(args.i, "rb").read()
	payload = {"image": image}

	# submit the request
	r = requests.post(args.u, files=payload).json()

	# ensure the request was successful
	if r["success"]:
	    # loop over the predictions and display them
	    for (i, result) in enumerate(r["predictions"]):
	        print("{}. {}: {:.4f}".format(i + 1, result["label"],
	            result["probability"]))
	# otherwise, the request failed
	else:
	    print("Request failed")

def main():
	POST(getparse())

if __name__ == '__main__':
	main()

```