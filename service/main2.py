

from flask import Flask, request, redirect, url_for,make_response,jsonify, render_template
from PIL import Image
from StringIO import StringIO
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import keras
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import Adam
import tensorflow as tf
import numpy as np
import requests
import PIL
import json
import model


app=Flask(__name__)

def read_image_from_url(url):
    response = requests.get(url, stream=True)

    img = Image.open(StringIO(response.content))
    img=img.resize((224,224), PIL.Image.ANTIALIAS).convert('RGB')
    #print img

    return img

@app.route('/api/v1/classify_image', methods=['POST'])
def classify_image():
    # print (request.json['imageurl'])
    # print (request.form.get('imageurl'))
    image_url = request.json['imageurl']
    if 'image_url' in request.json:
        print (image_url)
    else:
        print ("bad request")
    img = read_image_from_url(image_url)
    resp = model.predict(img)
    #return make_response(jsonify({'message': resp}), 200)
    return make_response(resp, 200)


@app.route("/", methods=['GET'])
def hello():
    """Return a friendly HTTP greeting."""
    return "Hello World!"
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)

# In[ ]:
