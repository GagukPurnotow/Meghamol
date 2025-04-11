from web3 import Web3
import time
from decimal import Decimal

# Setup koneksi RPC
RPC_URL = "https://carrot.megaeth.com/rpc"
web3 = Web3(Web3.HTTPProvider(RPC_URL))
chainId = web3.eth.chain_id

# Cek koneksi
if not web3.is_connected():
    print("❌ Gagal terhubung ke jaringan")
    exit()

print("✅ Berhasil terhubung ke jaringan MegaETH Testnet\n")

# Fungsi untuk simpan log ke file
def write_log(message):
    with open("result.txt", "a") as logfile:
        logfile.write(message + "\n")

# Fungsi kirim ETH
def send_all_ether(sender_address, sender_private_key, recipient_address):
    try:
        balance = web3.eth.get_balance(sender_address)
        readable_balance = web3.from_wei(balance, 'ether')
        print(f"💰 Saldo wallet: {readable_balance} ETH")

        if balance == 0:
            print("⚠️ Saldo 0, skip wallet ini.\n")
            write_log(f"{sender_address} | SKIP | Balance 0")
            return

        # Hitung gas
        gas_price = int(web3.eth.gas_price * Decimal(2.0))
        gas_limit = 21000
        gas_cost = gas_price * gas_limit

        amount_to_send = balance - gas_cost

        if amount_to_send <= 0:
            print("⚠️ Tidak cukup saldo untuk biaya gas.\n")
            write_log(f"{sender_address} | SKIP | Tidak cukup saldo gas")
            return

        # Build transaksi
        transaction = {
            'to': recipient_address,
            'value': amount_to_send,
            'gas': gas_limit,
            'maxFeePerGas': gas_price,
            'maxPriorityFeePerGas': gas_price,
            'nonce': web3.eth.get_transaction_count(sender_address),
            'chainId': chainId
        }

        # Sign dan kirim
        signed_txn = web3.eth.account.sign_transaction(transaction, sender_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_hex = web3.to_hex(tx_hash)

        # Tunggu receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        print(f"🚀 Transaksi sukses! Tx Hash: {tx_hex}\n")
        write_log(f"{sender_address} | SUCCESS | Tx Hash: {tx_hex}")

    except Exception as e:
        print(f"❌ Error: {e}\n")
        write_log(f"{sender_address} | ERROR | {e}")

# Main program
if __name__ == "__main__":
    recipient = input('🎯 Masukkan address EVM tujuan (MegaETH Testnet): ').strip()

    try:
        with open('pvkeylist.txt', 'r') as file:
            private_keys = [line.strip() for line in file if line.strip()]

        if not private_keys:
            print("⚠️ File pvkeylist.txt kosong! Tambahkan private key terlebih dahulu.")
            exit()

        print(f"🔑 Total wallet yang akan diproses: {len(private_keys)}\n")

        for idx, private_key in enumerate(private_keys, start=1):
            print(f"🚦 Memproses wallet {idx}...")
            sender = web3.eth.account.from_key(private_key)
            send_all_ether(sender.address, sender.key, web3.to_checksum_address(recipient))
            time.sleep(2)  # Delay biar tidak terlalu cepat

        print("✅ Semua wallet selesai diproses!")

    except FileNotFoundError:
        print("❌ File pvkeylist.txt tidak ditemukan! Pastikan file sudah tersedia.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")
