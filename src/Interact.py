from web3 import Web3
from Deploy import deploy_contract
import os

contract="./src/SimpleStorage.sol"
account = os.getenv("ANVIL_ACCOUNT")
private_key = os.getenv("ANVIL_PRIVATE_KEY")
provider=os.getenv("LOCAL_PROVIDER")
chain_id = 31337

connection= Web3(Web3.HTTPProvider(provider))

contract_address , abi = deploy_contract(contract,'SimpleStorage',account, private_key,provider,chain_id)

simple_storage=connection.eth.contract(address=contract_address,abi=abi)
nonce=connection.eth.get_transaction_count(account)

transaction=simple_storage.functions.set(150032145).build_transaction(
        {
            "chainId":chain_id,
            "gasPrice":connection.eth.gas_price,
            "from":account,
            "nonce":nonce
        }
    )
signed_txn=connection.eth.account.sign_transaction(transaction,private_key=private_key)

print("Updating value")
tx_hash=connection.eth.send_raw_transaction(signed_txn.raw_transaction)

tx_receipt=connection.eth.wait_for_transaction_receipt(tx_hash)
print("Updated")

updated_value=simple_storage.functions.get().call()
print(f"updated value={updated_value}")