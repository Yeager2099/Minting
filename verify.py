from web3 import Web3
from eth_account.messages import encode_defunct
import random

# Configuration constants
CONTRACT_ADDRESS = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
RPC_URL = "https://api.avax-test.network/ext/bc/C/rpc"  # Avalanche Fuji Testnet
ABI = [{"inputs":[{"internalType":"uint256","name":"nonce","type":"uint256"}],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"}]

def claim_nft():
    """ 
    Function to claim the NFT by calling the contract's claim() function.
    You need to call this function separately from your own implementation.
    """
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
    
    sk = "0x950dd91788d82b9ca2eb2417d2b26e9a3bea12d0f37b7b5e417ae87a1630f52c"
    account = w3.eth.account.from_key(sk)
    
    nonce = 1  # Using minimum nonce to get smallest tokenId
    tx = contract.functions.claim(nonce).build_transaction({
        'chainId': 43113,
        'gas': 200000,
        'gasPrice': w3.to_wei('25', 'gwei'),
        'nonce': w3.eth.get_transaction_count(account.address),
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, sk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash

def sign_challenge(challenge):
    """ 
    To actually claim the NFT you need to write code in your own file, or use another claiming method.
    Once you have claimed an NFT you can come back to this file, update the "sk" and submit to codio to 
    prove that you have claimed your NFT.
    
    This is the only line you need to modify in this file before you submit.
    """
    w3 = Web3()
    sk = "0x950dd91788d82b9ca2eb2417d2b26e9a3bea12d0f37b7b5e417ae87a1630f52c"
    
    acct = w3.eth.account.from_key(sk)
    signed_message = w3.eth.account.sign_message(challenge, private_key=acct.key)
    
    return acct.address, signed_message.signature

def verify_sig():
    """
    This is essentially the code that the autograder will use to test signChallenge.
    We've added it here for testing.
    """
    challenge_bytes = random.randbytes(32)
    challenge = encode_defunct(challenge_bytes)
    address, sig = sign_challenge(challenge)
    
    w3 = Web3()
    return w3.eth.account.recover_message(challenge, signature=sig) == address

if __name__ == '__main__':
    """
    Test your function
    """
    # Uncomment to claim NFT (should be done separately)
    # print("Claiming NFT...")
    # tx_hash = claim_nft()
    # print(f"✅ NFT claimed! Transaction hash: {tx_hash.hex()}")
    
    if verify_sig():
        print("You passed the challenge!")
    else:
        print("You failed the challenge!")
