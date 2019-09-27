import os

from ginger_sdk import Ginger


# Set these to your actual endpoint and API key
endpoint = os.getenv('GINGER_ENDPOINT')
api_key = os.getenv('GINGER_API_KEY')

# Get our client
client = Ginger.create_client(endpoint, api_key)

# Create our order without specifying a payment method
order = client.create_order({
    'amount': 250,  # Amount in cents
    'currency': 'EUR',
})

# Show the order URL where the user can select a payment method and initiate the transaction
print('Payment URL:', order['order_url'])
