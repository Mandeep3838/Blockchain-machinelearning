# Python Secure Decentralized Learning App

A Blockchain application with federated learning using neural networks.

## What is blockchain? How it is implemented? And how it works?

Please read the [step-by-step implementation tutorial](https://www.ibm.com/developerworks/cloud/library/cl-develop-blockchain-app-in-python/index.html) to get your answers :)

## What are neural networks? And how it works?

Please read the [step-by-step tutorial](https://www.tutorialspoint.com/artificial_neural_network/index.htm) to get your answers :)


## Instructions to run

Clone the project,

```sh
$ git clone https://github.com/Mandeep3838/Blockchain-machinelearning.git
```

Install the dependencies,

```sh
$ cd Blockchain-machinelearning
$ pip install -r requirements.txt
```

Start a blockchain-federated learning model,

```sh
$ chmod 777 miner_script.sh clients_script.sh kill_sessions.sh
$ ./miner_script.sh
```
On a different Terminal
```sh
$ ./clients_script.sh
```
## After this step

* Two instances of blockchain node are now up and running on port 8000,8001.
* Client nodes are running on ports {5000,5001,...,5010}
* Testing node is running on port 9000
* You can check results on the firefox browser
* Error files for each client and test node are saved in the working directory as blocks are added.
* For checking chain, refresh http://127.0.0.1:8000/chain


## Working Video

1. Posting some content

![image.png](https://github.com/satwikkansal/python_blockchain_app/raw/master/screenshots/1.png)

2. Requesting the node to mine

![image.png](https://github.com/satwikkansal/python_blockchain_app/raw/master/screenshots/2.png)

3. Resyncing with the chain for updated data

![image.png](https://github.com/satwikkansal/python_blockchain_app/raw/master/screenshots/3.png)

Default app takes two client nodes as malicious, you can increase the maliciousness by changing **z** variable in the clients_script.sh

Here's a sample scenario that you might wanna try,

```sh
# Make sure you set the FLASK_APP environment variable to node_server.py before running these nodes
# already running
$ flask run --port 8000 &
# spinning up new nodes
$ flask run --port 8001 &
$ flask run --port 8002 &
```

You can use the following cURL requests to register the nodes at port `8001` and `8002` with the already running `8000`.

```sh
curl -X POST \
  http://127.0.0.1:8001/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'
```

```sh
curl -X POST \
  http://127.0.0.1:8002/register_with \
  -H 'Content-Type: application/json' \
  -d '{"node_address": "http://127.0.0.1:8000"}'
```

This will make the node at port 8000 aware of the nodes at port 8001 and 8002, and make the newer nodes sync the chain with the node 8000, so that they are able to actively participate in the mining process post registration.

To update the node with which the frontend application syncs (default is localhost port 8000), change `CONNECTED_NODE_ADDRESS` field in the [views.py](/app/views.py) file.

Once you do all this, you can run the application, create transactions (post messages via the web inteface), and once you mine the transactions, all the nodes in the network will update the chain. The chain of the nodes can also be inspected by inovking `/chain` endpoint using cURL.

```sh
$ curl -X GET http://localhost:8001/chain
$ curl -X GET http://localhost:8002/chain
```

*PS: For consulting, you can reach out to me via Codementor (use [this link](https://www.codementor.io/satwikkansal?partner=satwikkansal) for free 10$ credits).*
