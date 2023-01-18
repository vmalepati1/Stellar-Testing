from stellar_sdk import Keypair
import requests

# Account 1
##pair = Keypair.random()
##print(f"Secret: {pair.secret}")
### Secret: SCBDNKUBCBMBPZUGQ4LGBEXLRF5WSPHH7ZI2OJMBN2CLIAKGJT6OCD73
##print(f"Public Key: {pair.public_key}")
### Public Key: GAXNHPN5KCSDHEM7KN2UCTR3OSGVNBM26C33ICQDZHGDHJJK3ES6F3NE

# Account 2
pair = Keypair.random()
print(f"Secret: {pair.secret}")
# Secret: SADWIQXRSDP4GRF7REQ2KNNZD64PATUAIYANLYGGO6YQ6IWKQP3KT57C
print(f"Public Key: {pair.public_key}")
# Public Key: GD6YBMHQKWXAFV34FSRQ6SZ2IGJ3JYY5B5A2Y574OU4ZIDD3PDV2DBD2

public_key = pair.public_key

response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")

if response.status_code == 200:
    print(f"SUCCESS! You have a new account :)\n{response.text}")
else:
    print(f"ERROR! Response: \n{response.text}")
