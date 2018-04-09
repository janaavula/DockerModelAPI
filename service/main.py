

from flask import Flask, request, redirect, url_for,make_response,jsonify, render_template
from PIL import Image
from StringIO import StringIO
import keras
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import Adam
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import numpy as np
import requests
import PIL
import json


app=Flask(__name__)
global model, graph

def init():
	model = load_model('/opt/app/vgg16tensorflowmodel.h5')

	#compile and evaluate loaded model
	# model.compile(optimizer=Adam(lr=0.0001),
    #             loss='categorical_crossentropy', metrics=['accuracy'])
	#loss,accuracy = model.evaluate(X_test,y_test)
	#print('loss:', loss)
	#print('accuracy:', accuracy)
	graph = tf.get_default_graph()

	return model,graph

model, graph = init()

def predict(imageone):



    #imageone = '/Users/jac812i/Documents/Imagerecognition/unknown/unknown/images?q=tbn:ANd9GcSTraBoazT_Rk9-BRdntEDaDvE2QWd2wimQuoZg4Ho-h9eFbliH.jpg'
    #img=image.load_img(imageone, target_size=(224, 224))
    img = image.img_to_array(imageone)
    print (img.shape)

    red=img[:,:,0]
    green=img[:,:,1]
    blue=img[:,:,2]

    # image_convert=np.array([red,green,blue]).reshape((224,224,3))
    # print (image_convert.shape)
    # image_convert = np.expand_dims(image_convert, axis=0)
    image_convert = np.expand_dims(img, axis=0)
    print (image_convert.shape)
    with graph.as_default():
        preds = model.predict(image_convert)
        print (preds[0])
        listpreds = []
        for i in preds[0]:
            listpreds.append('%.5f' %i)
        print (listpreds)

        #Labels as per folder structure
        labels = ["faucet","flowerpots","hammer","thermostats"]
        pred = dict(zip(labels, listpreds))
        bestpred = labels[np.argmax(preds[0])]
        print ("probabilties for each category", pred)
        print ("Model predicted image is ", bestpred)

        json_str = json.dumps(pred)

        print (json_str)

    return json_str

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
    resp = predict(img)
    #return make_response(jsonify({'message': resp}), 200)
    return make_response(resp, 200)


@app.route("/", methods=['GET'])
def hello():
    """Return a friendly HTTP greeting."""
    return "Hello World!"
    # return render_template('/opt/app/templates/index.html')
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)

# In[ ]:
