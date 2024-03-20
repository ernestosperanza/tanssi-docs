# 1. Add imports
from compile import abi
from web3 import Web3

# 2. Create web3.py provider
provider_rpc = {
    # Insert your RPC URL here
    "evm_appchain": "https://fraa-dancebox-3001-rpc.a.dancebox.tanssi.network",
}
web3 = Web3(Web3.HTTPProvider(provider_rpc["evm_appchain"]))

# 3. Create variables
account_from = {
    "private_key": "INSERT_YOUR_PRIVATE_KEY",
    "address": "INSERT_PUBLIC_ADDRESS_OF_PK",
}
contract_address = "INSERT_CONTRACT_ADDRESS"
value = 3

print(
    f"Calling the increment by { value } function in contract at address: { contract_address }"
)

# 4. Create contract instance
Incrementer = web3.eth.contract(address=contract_address, abi=abi)

# 5. Build increment tx
increment_tx = Incrementer.functions.increment(value).build_transaction(
    {
        "from": Web3.to_checksum_address(account_from["address"]),
        "nonce": web3.eth.get_transaction_count(
            Web3.to_checksum_address(account_from["address"])
        ),
    }
)

# 6. Sign tx with PK
tx_create = web3.eth.account.sign_transaction(increment_tx, account_from["private_key"])

# 7. Send tx and wait for receipt
tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Tx successful with hash: { tx_receipt.transactionHash.hex() }")
