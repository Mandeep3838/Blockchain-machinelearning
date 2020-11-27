from hashlib import sha256
import json, pickle
import numpy
import pandas
import scipy.spatial as sp
import random
import time

from flask import Flask, request
import requests
import backprop as bp

 
class Block:
    def __init__(self, index, wei, b, timestamp, previous_hash, nonce=0):
        self.index = index
        self.wei = wei
        self.b = b
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        # temp = self
        # temp.wei = self.wei.tolist()
        # temp.b = self.b.tolist()
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, 0, 0, 0, "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        self.unconfirmed_transactions = []
        return True

    @staticmethod
    def proof_of_work(block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block["hash"]
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block_hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        wei = []
        b = []
        k = 8
        aggr = 5

        # model averaging
        if len(self.unconfirmed_transactions) == 1:
            # transaction = self.unconfirmed_transactions[0]
            # wei = transaction["wei"]
            # b = transaction["b"]
            # print("Singly Mined")
            return False

        elif len(self.unconfirmed_transactions) > k:
            # nearest aggr aggregation

            W = []
            B = []
            for i in range(len(self.unconfirmed_transactions)):
                w = []
                b = []
                transaction = self.unconfirmed_transactions[i]
                for wei in transaction["wei"]:
                    temp_w = numpy.array(wei)
                    w.append(temp_w)
                for base in transaction["b"]:
                    temp_b = numpy.array(base)
                    b.append(temp_b)
                W.append(w)
                B.append(b)
            # averaging
            avg_w = []
            avg_b = []
            for i in range(len(W[0])):
                temp_w = W[0][i]/numpy.linalg.norm(W[0][i])       # normalized
                temp_b = B[0][i]/numpy.linalg.norm(B[0][i])       # normalized
                for z in range(1,len(W)):
                    temp_w = temp_w + W[z][i]/numpy.linalg.norm(W[z][i])           
                    temp_b = temp_b + B[z][i]/numpy.linalg.norm(B[z][i])
                temp_w = temp_w/len(self.unconfirmed_transactions)
                temp_b = temp_b/len(self.unconfirmed_transactions)
                avg_w.append(temp_w)
                avg_b.append(temp_b)
            score = []
            for z in range(len(W)):
                sk = 0
                for i in range(len(W[0])):
                    sk = sk + (1 - sp.distance.cdist(W[z][i]/numpy.linalg.norm(W[z][i]), avg_w[i], 'cosine')).sum()
                score.append(sk)
            indices = numpy.argsort(-numpy.array(score),kind='mergesort')[:aggr]
            print("Score of k ",score)
            # averaging of selected
            new_w = []
            new_b = []
            for i in range(len(W[indices[0]])):
                temp_w = W[indices[0]][i]
                temp_b = B[indices[0]][i]
                for z in range(1,len(indices)):
                    temp_w = temp_w + W[indices[z]][i]
                    temp_b = temp_b + B[indices[z]][i]
                temp_w = temp_w/aggr
                temp_b = temp_b/aggr
                new_w.append(temp_w)
                new_b.append(temp_b)
            
            wei = [] # back into list
            b = []
            for w in new_w:
                wei.append(w.tolist())
            for j in new_b:
                b.append(j.tolist())
            print("aggr Aggregated")

        # else: # averaging of all
        #     W = []
        #     B = []
        #     for i in range(len(self.unconfirmed_transactions)):
        #         w = []
        #         b = []
        #         transaction = self.unconfirmed_transactions[i]
        #         for wei in transaction["wei"]:
        #             temp_w = numpy.array(wei)
        #             w.append(temp_w)
        #         for base in transaction["b"]:
        #             temp_b = numpy.array(base)
        #             b.append(temp_b)
        #         W.append(w)
        #         B.append(b)
            
        #     new_w = []
        #     new_b = []
        #     for i in range(len(W[0])):
        #         temp_w = W[0][i]
        #         temp_b = B[0][i]
        #         for z in range(1,len(W)):
        #             temp_w = temp_w + W[z][i]
        #             temp_b = temp_b + B[z][i]
        #         temp_w = temp_w/len(self.unconfirmed_transactions)
        #         temp_b = temp_b/len(self.unconfirmed_transactions)
        #         new_w.append(temp_w)
        #         new_b.append(temp_b)
            
        #     wei = [] # back into list
        #     b = []
        #     for w in new_w:
        #         wei.append(w.tolist())
        #     for j in new_b:
        #         b.append(j.tolist())
            # print("Aggregated and Mined")
        else:
            return False    # less than k transactions

        new_block = Block(index=last_block.index + 1,
                          wei=wei,
                          b=b,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []

        return True


app = Flask(__name__)

# the node's copy of blockchain
blockchain = Blockchain()
blockchain.create_genesis_block()

# the address to other participating members of the network
peers = set()

# endpoint to submit a new transaction. This will be used by
# our application to add new data (posts) to the blockchain
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["wei", "b"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.time()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201


# endpoint to return the node's copy of the chain.
# Our application will be using this endpoint to query
# all the posts to display.
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain: 
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data,
                       "peers": list(peers)})


# endpoint to request the node to mine the unconfirmed
# transactions (if any). We'll be using it to initiate
# a command to mine from our application itself.
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    while(True):
        result = blockchain.mine()
        if not result:
            print("No transactions to mine or Less than k transactions")
        else:
            # Making sure we have the longest chain before announcing to the network
            chain_length = len(blockchain.chain)
            consensus()
            if chain_length == len(blockchain.chain):
                # announce the recently mined block to the network
                announce_new_block(blockchain.last_block)
            print("Block #{} is mined.".format(blockchain.last_block.index))
        time.sleep(random.randint(10,20))


# endpoint to add new peers to the network.
@app.route('/register_node', methods=['POST'])
def register_new_peers():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    # Add the node to the peer list
    peers.add(node_address[:-1])

    # Return the consensus blockchain to the newly registered node
    # so that he can sync
    return get_chain()


@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    """
    Internally calls the `register_node` endpoint to
    register current node with the node specified in the
    request, and sync the blockchain as well as peer data.
    """
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    # Make a request to register with remote node and obtain information
    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        # update chain and the peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return "Registration successful", 200
    else:
        # if something goes wrong, pass it on to the API response
        return response.content, response.status_code


def create_chain_from_dump(chain_dump):
    generated_blockchain = Blockchain()
    generated_blockchain.create_genesis_block()
    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            continue  # skip genesis block
        block = Block(block_data["index"],
                      block_data["wei"],
                      block_data["b"],
                      block_data["timestamp"],
                      block_data["previous_hash"],
                      block_data["nonce"])
        proof = block_data['hash']
        added = generated_blockchain.add_block(block, proof)
        if not added:
            raise Exception("The chain dump is tampered!!")
    return generated_blockchain


# endpoint to add a block mined by someone else to
# the node's chain. The block is first verified by the node
# and then added to the chain.
@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["wei"],
                  block_data["b"],
                  block_data["timestamp"],
                  block_data["previous_hash"],
                  block_data["nonce"])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


# endpoint to query unconfirmed transactions
@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)

def consensus():
    """
    Our naive consnsus algorithm. If a longer valid chain is
    found, our chain is replaced with it.
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)
    for node in peers:
        if node != str(request.host_url)[:-1]:
            response = requests.get('{}/chain'.format(node))
            length = response.json()['length']
            chain = response.json()['chain']
            if length > current_len and blockchain.check_chain_validity(chain):
                current_len = length
                longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False


def announce_new_block(block):
    """
    A function to announce to the network once a block has been mined.
    Other blocks can simply verify the proof of work and add it to their
    respective chains.
    """
    for peer in peers:
        if peer != str(request.host_url)[:-1]:
            url = "{}/add_block".format(peer)
            headers = {'Content-Type': "application/json"}
            requests.post(url,
                        data=json.dumps(block.__dict__, sort_keys=True),
                        headers=headers)

# Uncomment this line if you want to specify the port number in the code
#app.run(debug=True, port=8000)
