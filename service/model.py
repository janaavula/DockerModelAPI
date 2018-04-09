from PIL import Image
from StringIO import StringIO
import keras
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import Adam
import tensorflow as tf
import numpy as np
import requests
import PIL
import json
import os

model = load_model('/opt/app/vgg16tensorflowmodel.h5')
model.compile(optimizer=Adam(lr=0.0001),
            loss='categorical_crossentropy', metrics=['accuracy'])
graph = tf.get_default_graph()


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
