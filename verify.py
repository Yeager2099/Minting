from web3 import Web3
from eth_account.messages import encode_defunct
import random

def sign_challenge(challenge):
    w3 = Web3()
    
    # >>>>> 唯一需要修改的行 <<<<< 
    sk = "0x950dd91788d82b9ca2eb2417d2b26e9a3bea12d0f37b7b5e417ae87a1630f52c"
    
    acct = w3.eth.account.from_key(sk)
    signed_message = w3.eth.account.sign_message(challenge, private_key=acct.key)
    return acct.address, signed_message.signature

def verify_sig():
    challenge_bytes = random.randbytes(32)
    challenge = encode_defunct(challenge_bytes)
    address, sig = sign_challenge(challenge)
    return w3.eth.account.recover_message(challenge, signature=sig) == address

if __name__ == '__main__':
    if verify_sig():
        print("You passed the challenge!")
    else:
        print("You failed the challenge!")
