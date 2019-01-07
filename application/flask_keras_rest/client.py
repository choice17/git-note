# import the necessary packages
import requests
import argparse
import time
import datetime
# initialize the Keras REST API endpoint URL along with the input
# image path
KERAS_REST_API_URL = "http://localhost:5000/predict"
IMAGE_DIR = 'dog.jpg'


def getparse():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', type=str, default=IMAGE_DIR, help='input image dir')
	parser.add_argument('-u', type=str, default=KERAS_REST_API_URL, help='rest service ip')
	return parser.parse_args()

# load the input image and construct the payload for the request
def POST(args):
	image = open(args.i, "rb").read()
	payload = {"image": image}

	# submit the request
	ti = time.time()
	r = requests.post(args.u, files=payload).json()
	toc = time.time() - ti
	# ensure the request was successful
	if r["success"]:
	    # loop over the predictions and display them
	    for (i, result) in enumerate(r["predictions"]):
	        print("{}. {}: {:.4f}".format(i + 1, result["label"],
	            result["probability"]))
	# otherwise, the request failed
	else:
	    print("Request failed")
	print("[INFO] TIME: %s Total time needed to response: %.4f sec" % (datetime.datetime.now(), toc))
def main():
	POST(getparse())

if __name__ == '__main__':
	main()