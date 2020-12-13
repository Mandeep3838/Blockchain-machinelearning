# Python Secure Decentralized Learning App

A Blockchain application with federated learning model using neural networks.

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


## Working

1. Demo Video

![blockchain-machinelearning.mp4](https://github.com/Mandeep3838/Blockchain-machinelearning/raw/master/docs/blockchain-machinelearning.mp4)

2. Miner Node

![image.png](https://github.com/satwikkansal/python_blockchain_app/raw/master/screenshots/2.png)

3. Client Node

![image.png](https://github.com/satwikkansal/python_blockchain_app/raw/master/screenshots/3.png)

## Different Scenarios 

* Default app takes two client nodes as malicious, you can increase the maliciousness by changing **z** variable in the clients_script.sh
* Increasing Network (Requires Higher Computational power)
  * You can increase the miner and client nodes by increasing the limit of for loops in miner_script.sh, clients_script.sh
  * In Miner Script
    * Replace 8001 by 80xx
  * In Client Script
    * More curl lines to set up a network.
    * Add new peer in the peers array.
    * Replace 5010 by 50yy, 8001 by 80xx
    * Modify start and end variable, as the share of data available to each client from 1100 rows.
  * Run the bash script

## Documentation of Code

Present in the [docs]() directory

