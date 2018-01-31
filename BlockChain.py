import hashlib
import json
import flask
from time import time
from uuid import uuid4


class BlockChain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create Genesis block
        #
        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: int given by the Proof of Work algorithm
        :param previous_hash: (Optional) str Hash of previous Block

        :return: dict new block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Clear current transactions
        #
        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: str
        :param recipient: str
        :param amount: int

        :return: int The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        Proof of work is a problem that is "difficult" to solve, but
        "easy" to verify

        Simple Proof of Work:
            - Find a number y such that hash(x * y) contains 4 leading zeros
            - X is the previous y (proof)
            - Y is the new proof (solution)

        :param last_proof: int
        :return: int
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Return whether or not the give proof (int) is valid
        (i.e does the hash have 4 leading zeros)

        :param last_proof: int
        :param proof: int
        :return: Bool
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha3_256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """
        Calculate SHA-256 has of a block

        :param block: dict
        :return: str
        """

        # Ensure that the dict is ordered so hash calculations are consistent
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha3_256(block_string).hexdigest()

    @property
    def last_block(self):
        # returns the last block of the chain
        #
        return self.chain[-1]


# Setup the server
#
app = flask.Flask(__name__)

# Generate a unique address for this node
#
node_identifier = str(uuid4()).replace('-', '')

# Start the BlockChain
#
block_chain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    """
    1. Calculate the proof of work
    2. Reward the miner by adding a transaction granting them 1 coin
    3. Add the new block to the chain
    """

    # calculate the proof of work
    #
    last_block = block_chain.last_block
    last_proof = last_block['proof']
    proof = block_chain.proof_of_work(last_proof)

    # reward the miner sender is '0' for the server
    #
    block_chain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    # Add the new block to the chain
    #
    previous_hash = block_chain.hash(last_block)
    new_block = block_chain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': new_block['index'],
        'transactions': new_block['transactions'],
        'proof': new_block['proof'],
        'previous_hash': new_block['previous_hash']
    }

    return flask.jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = flask.request.get_json(force=True)

    # Check that all the data is there
    #
    if 'sender' not in values:
        return "Missing Sender", 400
    if 'recipient' not in values:
        return "Missing Recipient", 400
    if 'amount' not in values:
        return "Missing Amount", 400

    # Create a new transaction
    #
    index = block_chain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block{index}'}

    return flask.jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': block_chain.chain,
        'length': len(block_chain.chain),
    }
    return flask.jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
