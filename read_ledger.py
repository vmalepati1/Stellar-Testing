from stellar_sdk import Server

server = Server(horizon_url="https://horizon.stellar.org")

transactions = server.transactions().for_ledger(1399).call()
print(transactions)
