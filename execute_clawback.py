from stellar_sdk import Asset, Keypair, Network, Server, TransactionBuilder, SetOptions
from stellar_sdk import AuthorizationFlag, Clawback

# Configure Stellar SDK to talk to the horizon instance hosted by Stellar.org
# To use the live network, set the hostname to 'https://horizon.stellar.org'
server = Server(horizon_url="https://horizon-testnet.stellar.org")
# Use test network, if you need to use public network, please set it to `Network.PUBLIC_NETWORK_PASSPHRASE`
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

# Keys for accounts to issue and receive the new asset
issuing_keypair = Keypair.from_secret(
    "SCBDNKUBCBMBPZUGQ4LGBEXLRF5WSPHH7ZI2OJMBN2CLIAKGJT6OCD73"
)
issuing_public = issuing_keypair.public_key

distributor_keypair = Keypair.from_secret(
    "SADWIQXRSDP4GRF7REQ2KNNZD64PATUAIYANLYGGO6YQ6IWKQP3KT57C"
)
distributor_public = distributor_keypair.public_key

# Transactions require a valid sequence number that is specific to this account.
# We can fetch the current sequence number for the source account from Horizon.
issuing_account = server.load_account(issuing_public)
distributor_account = server.load_account(distributor_public)

# Create an object to represent the new asset
some_stock = Asset("Test123", issuing_public)

enable_clawback_transaction = (
    TransactionBuilder(
        source_account=issuing_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_operation(SetOptions(set_flags=AuthorizationFlag.AUTHORIZATION_CLAWBACK_ENABLED | AuthorizationFlag.AUTHORIZATION_REVOCABLE))
    .set_timeout(100)
    .build()
)

enable_clawback_transaction.sign(issuing_keypair)
clawback_transaction_resp = server.submit_transaction(enable_clawback_transaction)
print(f"Clawback Transaction Resp:\n{clawback_transaction_resp}")

# First, the receiving account must trust the asset
trust_transaction = (
    TransactionBuilder(
        source_account=distributor_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    #  The `changeTrust` operation creates (or alters) a trustline
    #  The `limit` parameter below is optional
    .append_change_trust_op(asset=some_stock, limit="1000")
    .set_timeout(100)
    .build()
)

trust_transaction.sign(distributor_keypair)
trust_transaction_resp = server.submit_transaction(trust_transaction)
print(f"Change Trust Transaction Resp:\n{trust_transaction_resp}")

# Second, the issuing account actually sends a payment using the asset.
payment_transaction = (
    TransactionBuilder(
        source_account=issuing_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_payment_op(
        destination=distributor_public,
        asset=some_stock,
        amount="10",
    )
    .build()
)
payment_transaction.sign(issuing_keypair)
payment_transaction_resp = server.submit_transaction(payment_transaction)
print(f"Payment Transaction Resp:\n{payment_transaction_resp}")

do_clawback_transaction = (
    TransactionBuilder(
        source_account=issuing_account,
        network_passphrase=network_passphrase,
        base_fee=100,
    )
    .append_operation(Clawback(some_stock, distributor_public, "5"))
    .set_timeout(100)
    .build()
)
do_clawback_transaction.sign(issuing_keypair)
do_clawback_resp = server.submit_transaction(do_clawback_transaction)
print(f"Do Clawback Transaction Resp:\n{do_clawback_resp}")
