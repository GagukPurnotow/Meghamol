from web3 import Web3
from decimal import Decimal

# --- Configuration ---
RPC_URL = "https://carrot.megaeth.com/rpc"
CHAIN_ID = 6342  # MegaETH testnet
GAS_LIMIT = 21000
BUFFER = 0.000005  # Biarkan sedikit buffer biar aman

# --- Setup Web3 ---
web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    print("[ERROR] Failed to connect to MegaETH network.")
    exit()

# --- Functions ---

def send_all_eth(sender_address, private_key, recipient_address):
    try:
        balance = web3.eth.get_balance(sender_address)
        readable_balance = web3.from_wei(balance, 'ether')
        print(f"[INFO] Sender balance: {readable_balance} ETH")

        if balance == 0:
            print("[WARNING] Balance is zero, skipping...")
            return

        gas_price = web3.eth.gas_price  # tanpa multiplier
        gas_cost = gas_price * GAS_LIMIT

        value = balance - gas_cost

        # Sisakan buffer
        buffer_wei = web3.to_wei(Decimal(BUFFER), 'ether')
        value -= buffer_wei

        if value <= 0:
            print("[WARNING] Not enough balance to cover gas fee, skipping...")
            return

        tx = {
            'to': recipient_address,
            'value': value,
            'gas': GAS_LIMIT,
            'gasPrice': gas_price,
            'nonce': web3.eth.get_transaction_count(sender_address),
            'chainId': CHAIN_ID
        }

        print(f"[PROCESS] Sending {web3.from_wei(value, 'ether')} ETH to {recipient_address}")

        signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(f"[SUCCESS] Tx sent! Hash: {web3.to_hex(tx_hash)}")

        # Optional: log to file
        with open('txlog.txt', 'a') as f:
            f.write(f"{sender_address} -> {recipient_address} | {web3.to_hex(tx_hash)}\n")

    except Exception as e:
        print(f"[ERROR] Error while sending ETH: {e}")

# --- Main ---
def main():
    recipient = input("Input address EVM recipient MegaETH testnet: ").strip()

    try:
        with open('pvkeylist.txt', 'r') as file:
            private_keys = file.read().splitlines()

        print(f"\n[INFO] Total wallets loaded: {len(private_keys)}\n")

        for idx, private_key in enumerate(private_keys, start=1):
            sender_account = web3.eth.account.from_key(private_key)
            print(f"[{idx}/{len(private_keys)}] Processing wallet: {sender_account.address}")
            send_all_eth(sender_account.address, private_key, web3.to_checksum_address(recipient))
            print("------------------------------------------------------------\n")

    except FileNotFoundError:
        print("[ERROR] File 'pvkeylist.txt' not found.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
