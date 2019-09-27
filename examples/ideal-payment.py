import os

from pprint import pprint

from ginger_sdk import Ginger


# Set these to your actual endpoint and API key
endpoint = os.getenv('GINGER_ENDPOINT')
api_key = os.getenv('GINGER_API_KEY')

# Get our client
client = Ginger.create_client(endpoint, api_key)

# Get the issuers
pprint(client.get_ideal_issuers())

# Create our order, indicating we want an iDEAL payment
order = client.create_order({
    'amount': 250,  # Amount in cents
    'currency': 'EUR',
    'transactions': [{
        'payment_method': 'ideal',
        'payment_method_details': {
            'issuer_id': 'INGBNL2A',
        },
    }]
})

# Show the payment URL of the transaction where the user can pay
print('Payment URL:', order['transactions'][0]['payment_url'])
