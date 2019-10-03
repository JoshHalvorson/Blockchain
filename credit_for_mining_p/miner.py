import hashlib
import requests
import json
import sys
from uuid import uuid4

# TODO: Implement functionality to search for a proof
def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Find a number p such that hash(last_block_string, p) contains 6 leading
    zeroes
    :return: A valid proof for the provided block
    """
    # return proof
    block_string = json.dumps(block, sort_keys=True).encode()
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    # return True or False
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    # print(guess_hash)

    return guess_hash[:2] == '00'


if __name__ == '__main__':
    try:
        with open('my_id.txt', 'r') as f:
            miner_id = f.readline().strip()
    except FileNotFoundError:
        new_m_id = str(uuid4()).replace('-', '')
        with open('my_id.txt', 'a+') as f:
            f.write(new_m_id)
            f.flush()
            f.seek(0)
            miner_id = f.readline().strip()

    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5002"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        data = requests.get(url=node + '/last_block').json()
        block = data['last_block']
        new_proof = proof_of_work(block)
        # print(new_proof)
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        json_proof = {'proof': new_proof, "miner_id": miner_id}

        mine_request = requests.post(url=node + '/mine', json=json_proof)
        # print(mine_request.json()['message'])
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if mine_request.json()['message'] == 'New Block Forged':
            coins_mined += 1
            print('Coins mined: ', coins_mined)
        pass
