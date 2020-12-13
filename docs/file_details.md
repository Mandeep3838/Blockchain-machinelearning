# Flask Apps
## Miner
Code Present in node_server.py.

### Useful Functions and Classes
* Class **Blockchain**
    * Initialize the chain
    * Functions
        * genesis_block- Create 1st block
        * last_block- Return recent block
        * add_block- check proof and add block in chain
        * proof_of_work- Computes the hash 
        * is_valid_proof- Validate hash and difficulty
        * add_new_transaction- Add unconfirmed transaction
        * check_chain_validity- Checks Validity of entire chain
        * mine
            * Collect all unconfirmed transactions
            * Aggregate transactions using filtering algorithms
            * Computing hash
            * Appending Block
* Class **Block**
    * Initialize the Block
    * Function to compute Sha-256 hash

### Endpoints
* new_transaction() - Accept transaction from client and save in unconfirmed transaactions
* chain() - Send the current chain.
* mine() - Start mining at this node.
* register_new_peers() - Link with other miners in the network.
* create_chain_from_dump() - This function creates a copy of chain from another miner and uses it.
* verify_and _add_block() - Validate a single block and add.
* get_pending_tx() - Return the unconfirmed transactions.
* consensus() - Establish consensus before adding the block
* announce_new_block() - Once block is mined, broadcast this block to network.

# Clients
Code present in app/views.py

### Functions
* Initialize()
    * Construct a Neural Network model
    * Connect to peers
* fetch_posts()
    * Fetch weights from the connected Miner
    * Replace Neural Network weights with these weights.
    * Calculate error
* timestamp_to_string() - Return the current timestamp.
### Endpoints
* index() - Render the fetched results to the client interface.
* submit()
    *  Train the Neural Network model
    *  Send weights to the miners
* getpeers() - Render the list of connected miners.