from flask import Flask, jsonify, request

import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from imageio import imread
import numpy as np
import tensorflow as tf
from io import BytesIO

from PIL import Image
import re
import time
import base64

from random import randint

dir_path = os.path.dirname(os.path.realpath(__file__))
MODEL_DETECT_PATH = dir_path + '/model/frozen_inference_graph.pb'

cred = credentials.Certificate('./it-proj-backend-250602-58ddd0292162.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
app = Flask(__name__)

menu = {1: {'id': 1, 'name': 'person'}, 2: {'id': 2, 'name': 'bicycle'}, 3: {'id': 3, 'name': 'car'}, 4: {'id': 4, 'name': 'motorcycle'}, 5: {'id': 5, 'name': 'airplane'}, 6: {'id':
                                                                                                                                                                                6, 'name': 'bus'}, 7: {'id': 7, 'name': 'train'}, 8: {'id': 8, 'name': 'truck'}, 9: {'id': 9, 'name': 'boat'}, 10: {'id': 10, 'name': 'traffic light'}, 11: {'id': 11, 'name':
                                                                                                                                                                                                                                                                                                                                             'fire hydrant'}, 13: {'id': 13, 'name': 'stop sign'}, 14: {'id': 14, 'name': 'parking meter'}, 15: {'id': 15, 'name': 'bench'}, 16: {'id': 16, 'name': 'bird'}, 17: {'id': 17,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  'name': 'cat'}, 18: {'id': 18, 'name': 'dog'}, 19: {'id': 19, 'name': 'horse'}, 20: {'id': 20, 'name': 'sheep'}, 21: {'id': 21, 'name': 'cow'}, 22: {'id': 22, 'name': 'elephant'}, 23: {'id': 23, 'name': 'bear'}, 24: {'id': 24, 'name': 'zebra'}, 25: {'id': 25, 'name': 'giraffe'}, 27: {'id': 27, 'name': 'backpack'}, 28: {'id': 28, 'name': 'umbrella'}, 31: {'id': 31, 'name': 'handbag'}, 32: {'id': 32, 'name': 'tie'}, 33: {'id': 33, 'name': 'suitcase'}, 34: {'id': 34, 'name': 'frisbee'}, 35: {'id': 35, 'name': 'skis'}, 36:
        {'id': 36, 'name': 'snowboard'}, 37: {'id': 37, 'name': 'sports ball'}, 38: {'id': 38, 'name': 'kite'}, 39: {'id': 39, 'name': 'baseball bat'}, 40: {'id': 40, 'name': 'baseball glove'}, 41: {'id': 41, 'name': 'skateboard'}, 42: {'id': 42, 'name': 'surfboard'}, 43: {'id': 43, 'name': 'tennis racket'}, 44: {'id': 44, 'name': 'bottle'}, 46: {'id': 46, 'name': 'wine glass'}, 47: {'id': 47, 'name': 'cup'}, 48: {'id': 48, 'name': 'fork'}, 49: {'id': 49, 'name': 'knife'}, 50: {'id': 50, 'name': 'spoon'}, 51: {'id': 51, 'name': 'bowl'}, 52: {'id': 52, 'name': 'banana'}, 53: {'id': 53, 'name': 'apple'}, 54: {'id': 54, 'name': 'sandwich'}, 55: {'id': 55, 'name': 'orange'}, 56: {'id': 56, 'name': 'broccoli'}, 57: {'id': 57, 'name': 'carrot'}, 58: {'id': 58, 'name': 'hot dog'}, 59: {'id': 59, 'name': 'pizza'}, 60: {'id': 60, 'name': 'donut'}, 61: {'id': 61, 'name': 'cake'},
        62: {'id': 62, 'name': 'chair'}, 63: {'id': 63, 'name': 'couch'}, 64: {'id': 64, 'name': 'potted plant'}, 65: {'id': 65, 'name': 'bed'}, 67: {'id': 67, 'name': 'dining table'}, 70: {'id': 70, 'name': 'toilet'}, 72: {'id': 72, 'name': 'tv'}, 73: {'id': 73, 'name': 'laptop'}, 74: {'id': 74, 'name': 'mouse'}, 75: {'id': 75, 'name': 'remote'}, 76: {'id': 76, 'name': 'keyboard'}, 77: {'id': 77, 'name': 'cell phone'}, 78: {'id': 78, 'name': 'microwave'}, 79: {'id': 79, 'name': 'oven'}, 80: {'id': 80, 'name': 'toaster'}, 81: {'id': 81, 'name': 'sink'}, 82: {'id': 82, 'name': 'refrigerator'}, 84: {'id': 84, 'name': 'book'}, 85: {'id': 85, 'name': 'clock'}, 86: {'id': 86, 'name': 'vase'}, 87: {'id':
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              87, 'name': 'scissors'}, 88: {'id': 88, 'name': 'teddy bear'}, 89: {'id': 89, 'name': 'hair drier'}, 90: {'id': 90, 'name': 'toothbrush'}}


def getI420FromBase64(b64in):
    """ Convert image from a base64 bytes stream to an image. """
    base64_data = b64in
    print(base64_data)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img


def readLabels():
    # Read each line of label file and strip \n
    labels = [label.rstrip('\n') for label in open(LABEL_PATH)]
    return labels


def apiResponseCreator_det(inputs, outputs):
    return dict(list(zip(inputs, outputs)))


def apiResponseCreator(labels, classifications):
    return dict(zip(labels, classifications))


def printTensors(model_file):
    # read protobuf into graph_def
    with tf.gfile.GFile(model_file, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # import graph_def
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def)

    # print operations
    for operation in graph.get_operations():
        print(operation.name)


@app.route('/')
def hello_world():
    return "compu-global-hyper-mega-net was here!"


@app.route('/items/add', methods=['POST'])
def addItem():
    data = request.get_json()
    db.collection(u'items').add(data)
    return str(data)


@app.route('/items/')
def getAllItems():
    items = db.collection(u'items').stream()
    itemstr = ''
    for item in items:

        itemstr += str(item.to_dict()) + '\n'
    return itemstr


@app.route('/detection', methods=['POST'])
def detection():
    data = request.get_json()

    datastring = data['image']
    print(type(datastring))
    # Load in an image to object detect and preprocess it
    img_data = getI420FromBase64(datastring)

    # img_data = Image.open(img_data)

    x_input = np.expand_dims(img_data, axis=0)  # add an extra dimention.

    # Setting initial detection time, so execution time can be calculated.
    t_det = time.time()

    # Get the predictions (output of the softmax) for this image
    tf_results_det = sess_det.run(
        [output_tensor_det, detection_boxes, detection_scores, detection_num], {input_tensor_det: x_input})

    dt_det = time.time() - t_det
    app.logger.info("Execution time: %0.2f" % (dt_det * 1000.))

    # Different results arrays
    predictions_det = tf_results_det[0]
    prediction_scores_det = tf_results_det[2]
    prediction_boxes_det = tf_results_det[1]
    prediction_num_det = tf_results_det[3]

    threshold = 0.85

    num = int(prediction_num_det)
    predict_list = predictions_det[0].astype(int).tolist()
    scores = prediction_scores_det[0]
    label = []

    for i in range(num):

        if scores[i] > threshold:
            prediction_label = predict_list[i]
            obj_name = menu[prediction_label]['name']

            label.append(obj_name)

    print("number and list of items that above the threshold")
    print(len(label))
    print(label)
    return label[0]


##################################################
# Starting the server
##################################################


if __name__ == '__main__':
    print('Starting TensorFlow Server')

    print('Configuring TensorFlow Graph..')
    # Create the session that we'll use to execute the model
    sess_config = tf.ConfigProto(
        log_device_placement=False,
        allow_soft_placement=True
    )

    print('Loading Model...')
    # G Read the graph definition file
    with open(MODEL_DETECT_PATH, 'rb') as k:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(k.read())

    # G Load the graph stored in `graph_def` into `graph`
    graph = tf.Graph()
    with graph.as_default():
        tf.import_graph_def(graph_def, name='')

    # G Enforce that no new nodes are added
    graph.finalize()

    sess_det = tf.Session(graph=graph, config=sess_config)

    print('Done.')

    input_op_det = graph.get_operation_by_name(
        'image_tensor')  # mport/Preprocessor/map/Shape
    input_tensor_det = input_op_det.outputs[0]
    output_op_det = graph.get_operation_by_name(
        'detection_classes')  # or num_detections
    output_tensor_det = output_op_det.outputs[0]

    detection_boxes_op = graph.get_operation_by_name('detection_boxes')
    detection_boxes = detection_boxes_op.outputs[0]
    detection_scores_op = graph.get_operation_by_name('detection_scores')
    detection_scores = detection_scores_op.outputs[0]
    detection_num_op = graph.get_operation_by_name('num_detections')
    detection_num = detection_num_op.outputs[0]

    app.run(debug=True, host='0.0.0.0')
