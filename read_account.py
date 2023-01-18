from stellar_sdk import Server

server = Server("https://horizon-testnet.stellar.org")
public_key = "GAXNHPN5KCSDHEM7KN2UCTR3OSGVNBM26C33ICQDZHGDHJJK3ES6F3NE"

account = server.accounts().account_id(public_key).call()

for balance in account['balances']:
    print(f"Type: {balance['asset_type']}, Balance: {balance['balance']}")

transactions = server.transactions().for_account(public_key).limit(2).call()

print(transactions)

# Print previous and next links
print(transactions['_links']['prev'])
print(transactions['_links']['next'])

# Get details of transaction

# Print account ID of friendbot
print(transactions['_embedded']['records'][0]['source_account'])
