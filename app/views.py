import datetime
import json
import backprop as bp 

import numpy
import pandas
import os
import time
import requests
from flask import render_template, redirect, request

from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.
CONNECTED_NODE_ADDRESS = set()

posts = []


peer = os.environ.get('PEER')
start_ind = int(os.environ.get('START_IND'))
end_ind = int(os.environ.get('END_IND'))

# import dataset
df = pandas.read_csv("data.csv")
data = df[start_ind:end_ind]

X = data.drop('charges', axis=1)
y = data['charges']
y = numpy.array(y)
y = y.reshape((len(y), 1))

# Preparing the NumPy array of the inputs.
data_inputs = numpy.array(X)
data_outputs = numpy.array(y)

data_inputs = data_inputs.T
data_outputs = data_outputs.T

mean = numpy.mean(data_inputs, axis = 1, keepdims=True)
std_dev = numpy.std(data_inputs, axis = 1, keepdims=True)
data_inputs = (data_inputs - mean)/std_dev
num_inputs = 12

description = [{"num_nodes" : 12, "activation" : "relu"},
               {"num_nodes" : 1, "activation" : "relu"}]

NN_model = bp.NeuralNetwork(description,num_inputs,"mean_squared", data_inputs, data_outputs, learning_rate=0.001)

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
        for peer in chain["peers"]:
            CONNECTED_NODE_ADDRESS.add(peer)
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
        error = NN_model.calc_accuracy(data_inputs, data_outputs, "RMSE")
        content["error"] = error
        content["index"] = last_block["index"]
        content["timestamp"] = last_block["timestamp"]
        print("Error from model: {error}".format(error=error))
        found = False
        for x in posts:
            if x["index"] == content["index"]:
                found = True
        if(not found):
            posts.append(content)
        posts = sorted(posts, key=lambda k: k['timestamp'],
                       reverse=True)


@app.route('/')
def index():
    global posts
    fetch_posts()
    return render_template('index.html',
                           title='YourNet: Decentralized '
                                 'content sharing',
                           posts=posts,
                           node_address=list(CONNECTED_NODE_ADDRESS)[0],
                           readable_time=timestamp_to_string)


@app.route('/submit', methods=['GET'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    global NN_model,CONNECTED_NODE_ADDRESS
    # post_content = request.form["content"]
    # author = request.form["author"]
    while(True):
        NN_model.train(1000)
        wei = []
        b = []
        for i in range(len(NN_model.layers)):
            wei.append(NN_model.layers[i].W.tolist())
            b.append(NN_model.layers[i].b.tolist())
        post_object = {
            'wei': wei,
            'b': b,
        }

        # Submit a transaction to all peers
        for peer in CONNECTED_NODE_ADDRESS:
            new_tx_address = "{}/new_transaction".format(peer)

            requests.post(new_tx_address,
                    json=post_object,
                    headers={'Content-type': 'application/json'})
        time.sleep(20)
    

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

@app.route('/getpeers', methods=['GET'])
def get_peers():
    return json.dumps({"peers": list(CONNECTED_NODE_ADDRESS)})
