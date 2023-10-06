import os
import time
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware, construct_sign_and_send_raw_middleware

# Initialize Web3 with your Ethereum node provider URL
web3 = Web3(Web3.HTTPProvider('https://api.sepolia.kroma.network/'))

# Load environment variables
load_dotenv()
MNEMONIC = os.getenv("MNEMONIC")

# Account Setup
web3.eth.account.enable_unaudited_hdwallet_features()
main_account = web3.eth.account.from_mnemonic(MNEMONIC, account_path="m/44'/60'/0'/0/0")
web3.eth.default_account = main_account.address

# Contract addresses
router_address = ""
weth_address = ""

# Contract ABI
router_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"}
        ],
        "name": "deposit",
        "outputs": [
            {"internalType": "uint256", "name": "amount0", "type": "uint256"},
            {"internalType": "uint256", "name": "amount1", "type": "uint256"}
        ],
        "stateMutability": "payable",
        "type": "function"
    }
]

def calculate_eth_amount(index):
    # Replace this with your own logic to calculate the ETH amount based on the index or any other criteria
    return 0.00001  # Return a constant value of 0.0001 ETH for each transaction

def wrap_eth_to_weth_batch(gas_price, delay, max_retries=3):
    delay = int(delay)
    
    for amount in range(num_transactions):
        retries = 0
        while retries < max_retries:
            try:
                # Amount in ETH to wrap
                eth_amount = calculate_eth_amount(amount)
                amount_wei = web3.to_wei(eth_amount, 'ether')

                # Create contract instance
                router_contract = web3.eth.contract(address=router_address, abi=router_abi)

                # Get current base fee using EIP-1559
                base_fee = web3.eth.gas_price

                # Set maximum fee and maximum priority fee
                max_fee = 5 * base_fee
                max_priority_fee = 5 * base_fee

                # Set the desired transaction fee
                transaction_fee = 0.0001388300013883  # ETH

                # Calculate the gas price based on the desired transaction fee
                gas_price = max(base_fee, min(transaction_fee / eth_amount, max_fee - max_priority_fee) + max_priority_fee)

                # Wrap ETH to WETH
                start_time = time.time()

                wrap_tx = router_contract.functions.deposit(main_account.address).build_transaction({
                    'from': main_account.address,
                    'gas': 44866,
                    'gasPrice': gas_price,
                    'nonce': web3.eth.get_transaction_count(main_account.address),
                    'value': amount_wei,
                })
                signed_wrap_tx = main_account.sign_transaction(wrap_tx)
                tx_hash = web3.eth.send_raw_transaction(signed_wrap_tx.rawTransaction)
                tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

                end_time = time.time()

                print("-------------------------------------------------")
                print("Transaction Information")
                print("This is a Kroma Sepolia testnet transaction only")
                print("Tokens minted")
                print(f"From: {main_account.address}")
                print(f"To: {router_address}")
                print(f"Method Id: e1fffcc4")
                print(f"Validator Address: {main_account.address}")
                print("Transaction sent. Hash:", tx_hash.hex())
                print(f"Status: {'Success' if tx_receipt['status'] == 1 else 'Failed'}")
                print(f"Block: {tx_receipt['blockNumber']}")
                print(f"Value: {eth_amount} ETH")
                print(f"Transaction Fee: {tx_receipt['gasUsed'] * gas_price / 1e9} ETH")
                print(f"Gas Price: {gas_price} Wei")
                print(f"Base: {base_fee} Wei")
                print(f"Max: {max_fee} Wei")
                print(f"Max priority: {max_priority_fee} Wei")
                print(f"Execution Time: {end_time - start_time:.2f} seconds")


                time.sleep(delay)
                break  # Break the retry loop if the transaction is successful

            except Exception as e:
                print(f"Error occurred: {str(e)}")
                retries += 1
                print(f"Retrying transaction ({retries}/{max_retries})")
                time.sleep(delay)

        if retries == max_retries:
            print(f"Max retries reached. Skipping transaction for amount: {amount}")
# Set the loop parameters
num_transactions = 10000  # Number of transactions to send
delay = 2  # Delay in seconds between transactions
gas_price = 5  # Adjust the gas price value as per your needs
for i in range(num_transactions):
    # Execute the wrapping transaction with error handling and retries
    wrap_eth_to_weth_batch(gas_price, delay)

    # Delay between transactions
    time.sleep(delay)

