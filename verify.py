from web3 import Web3
from eth_account.messages import encode_defunct
import random

# ===== 配置区块 =====
CONTRACT_ADDRESS = "0x85ac2e065d4526FBeE6a2253389669a12318A412"
RPC_URL = "https://api.avax-test.network/ext/bc/C/rpc"  # Avalanche Fuji Testnet
ABI = [
    {"inputs":[{"internalType":"uint256","name":"nonce","type":"uint256"}],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},
    {"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}
]

# ===== 账户配置 =====
# 使用您提供的测试账户（仅用于开发环境）
sk = "0x950dd91788d82b9ca2eb2417d2b26e9a3bea12d0f37b7b5e417ae87a1630f52c"
account = Web3().eth.account.from_key(sk)

# ===== 核心函数 =====
def claim_nft():
    """强制Claim NFT并返回交易状态"""
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
    
    try:
        # 动态获取Gas价格
        current_gas_price = w3.eth.gas_price
        nonce = random.randint(1, 1000)  # 随机nonce避免冲突
        
        tx = contract.functions.claim(nonce).build_transaction({
            'chainId': 43113,
            'gas': 300000,
            'gasPrice': int(current_gas_price * 1.2),  # 加价20%确保快速确认
            'nonce': w3.eth.get_transaction_count(account.address),
            'from': account.address
        })
        
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        print(f"✅ NFT Claim成功！区块: {receipt.blockNumber}")
        print(f"交易详情: https://testnet.snowtrace.io/tx/{tx_hash.hex()}")
        return True
        
    except Exception as e:
        print(f"❌ 交易失败: {str(e)}")
        return False

def check_nft_ownership():
    """验证账户是否持有NFT"""
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
    
    try:
        balance = contract.functions.balanceOf(account.address).call()
        print(f"当前NFT余额: {balance}")
        return balance > 0
    except Exception as e:
        print(f"❌ 查询失败: {str(e)}")
        return False

def sign_challenge(challenge):
    """签名验证函数（必须保留原始结构）"""
    signed_message = account.sign_message(challenge)
    return account.address, signed_message.signature

def verify_sig():
    """系统验证函数（勿修改）"""
    challenge_bytes = random.randbytes(32)
    challenge = encode_defunct(challenge_bytes)
    address, sig = sign_challenge(challenge)
    return Web3().eth.account.recover_message(challenge, signature=sig) == address

# ===== 主流程 =====
if __name__ == '__main__':
    print("=== Avalanche NFT验证系统 ===")
    print(f"验证账户: {account.address}")
    
    # 阶段1: NFT操作验证
    if not check_nft_ownership():
        print("⚠️ 未检测到NFT，正在自动Claim...")
        if not claim_nft():
            print("❌ 请手动Claim后重试")
            exit(1)
            
        # 等待链上确认
        import time
        time.sleep(30)
        
        if not check_nft_ownership():
            print("❌ NFT仍未到账，请检查交易记录")
            exit(1)
    
    # 阶段2: 签名验证
    if verify_sig():
        print("🎉 所有验证通过！请提交代码")
    else:
        print("❌ 签名验证失败，请检查私钥配置")
