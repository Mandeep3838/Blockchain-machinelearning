from hashlib import sha256
import json, pickle
import numpy
import pandas
import scipy.spatial as sp
import random
import time
import os

from flask import Flask, request
import requests
import backprop as bp


app = Flask(__name__)

CONNECTED_NODE_ADDRESS = set()

posts = []
peer = os.environ.get('PEER')
file_name = os.environ.get('ERROR_FILE')

# Test Dataset
df = pandas.read_csv("data.csv")
data_full = df[1100:]

X_full = data_full.drop('charges', axis=1)
y_full = numpy.array(data_full['charges'])
y_full = y_full.reshape((len(y_full), 1))


data_inputs_full = numpy.array(X_full).T
data_outputs_full = numpy.array(y_full).T

mean_full = numpy.mean(data_inputs_full, axis=1, keepdims=True)
std_dev_full = numpy.std(data_inputs_full, axis=1, keepdims=True)

for i in range(data_inputs_full.shape[0]):
    if std_dev_full[i] != 0:
        data_inputs_full[i] = (data_inputs_full[i] - mean_full[i])/std_dev_full[i]
    else:
        data_inputs_full[i] = data_inputs_full[i] - mean_full[i]

num_inputs = 12

description = [{"num_nodes" : 12, "activation" : "relu"},
               {"num_nodes" : 1, "activation" : "relu"}]

NN_model = bp.NeuralNetwork(description,num_inputs,"mean_squared", data_inputs_full, data_outputs_full, learning_rate=0.001)

CONNECTED_NODE_ADDRESS.add(peer)

def fetch_posts():
    """
    Function to fetch the chain from a blockchain node, parse the
    data and store it locally.
    """
    global NN_model, posts, CONNECTED_NODE_ADDRESS
    get_chain_address = "{}/chain".format(list(CONNECTED_NODE_ADDRESS)[0])
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        content = dict()
        chain = json.loads(response.content)
        full_chain = chain["chain"]
        last_block = full_chain[-1]
        if(last_block["wei"] != 0 and last_block["b"] != 0):
            # convert to ndarray
            wei = []
            b = []
            for w in last_block["wei"]:
                wei.append(numpy.array(w))
            for bases in last_block["b"]:
                b.append(numpy.array(bases))
            for i in range(len(NN_model.layers)):
                NN_model.layers[i].W = wei[i]
                NN_model.layers[i].b = b[i]
        
        NN_model.forward_pass()
        error_full = NN_model.calc_accuracy(data_inputs_full, data_outputs_full, "RMSE")
        content["error"] = error_full
        content["index"] = last_block["index"]
        content["timestamp"] = last_block["timestamp"]
        found = False
        for x in posts:
            if x["index"] == content["index"]:
                found = True
        if(not found):
            posts.append(content)
            # write to file
            f = open("9000_error_test" + str(file_name) + ".csv","a")
            f.write(str(last_block["index"]) + "," + str(error_full) + '\n')
            f.close()
        posts = sorted(posts, key=lambda k: k['timestamp'],
                       reverse=True)

@app.route('/test')
def index():
    global posts
    while(True):
        fetch_posts()
        time.sleep(5)
    return "Successfull", 200