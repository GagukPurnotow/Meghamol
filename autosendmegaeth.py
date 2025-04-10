from web3 import Web3
import requests, json, time, secrets
from decimal import Decimal

web3 = Web3(Web3.HTTPProvider("https://carrot.megaeth.com/rpc"))
chainId = web3.eth.chain_id
# Ensure the connection is made
if not web3.is_connected():
    print("Failed to connect to network")
    exit()
            
# Send all ether from one address to another
def send_all_ether(sender_address, sender_private_key, recipient_address):
    try:
        # Get sender's balance
        balance = web3.eth.get_balance(sender_address)
        print(f"Sender balance: {web3.from_wei(balance, 'ether')} ETH")
        
        # Use the sender's full balance, excluding the gas cost
        # Get current gas fee using EIP-1559 parameters
        gas_data = int(web3.eth.gas_price*Decimal(2.0))  # For EIP-1559: web3.eth.gas_price returns maxFeePerGas
        max_fee_per_gas = gas_data  # You can adjust this if you want to include more logic
        
        # Standard gas limit for ETH transfer
        gas_limit = 22000
        
        # Calculate the gas cost
        gas_cost = gas_limit * max_fee_per_gas
        
        # Subtract the gas cost from the balance to ensure the sender has enough ETH
        amount_to_send = balance - gas_cost
        
        if amount_to_send <= 0:
            print(f"Not enough balance to cover gas cost. Balance: {web3.from_wei(balance, 'ether')} ETH")
            return
        
        # Build the transaction with EIP-1559 parameters
        transaction = {
            'to': recipient_address,
            'value': amount_to_send,  # Send all Ether after gas cost
            'gas': 21000,
            'maxFeePerGas': max_fee_per_gas,
            'maxPriorityFeePerGas': max_fee_per_gas,
            'nonce': web3.eth.get_transaction_count(sender_address),
            'chainId': web3.eth.chain_id  # Automatically use the current chain ID
        }
        
        # Send the transaction
        print(f"Processing send {web3.from_wei(amount_to_send, 'ether')} ETH To {recipient_address}")
        tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(transaction, sender_private_key).rawTransaction)
        
        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction sent! Tx Hash: {web3.to_hex(tx_hash)}")
    
    except Exception as e:
        print(f"Error while sending eth: {e}")

recipient = input('input address evm recipient megaeth testnet : ')
with open('pvkeylist.txt', 'r') as file:
    try:
        local_data = file.read().splitlines()
        for pvkeylist in local_data:
            sender = web3.eth.account.from_key(pvkeylist)
            send_all_ether(sender.address, sender.key, web3.to_checksum_address(recipient))
    except Exception as e:
        print(str(e))