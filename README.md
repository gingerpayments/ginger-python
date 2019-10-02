# Ginger Python bindings

[![Build Status](https://travis-ci.org/gingerpayments/ginger-php.svg)](https://travis-ci.org/gingerpayments/ginger-python.svg)
[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/gingerpayments/ginger-php/blob/master/LICENSE)

## Requirements

* Python 3.6 or later
* requests 2.20 or later

## Installation

You can install the Python bindings from PyPI:

```shell script
pip install ginger-sdk
```

You can also use the Python bindings without using the Python Package Index by placing the ginger_sdk directory
somewhere in your `PYTHONPATH`.

## Getting started

First create a new API client with your API key and API endpoint:

```python
from ginger_sdk import Ginger

client = Ginger.create_client('https://api.example.com', 'your-api-key')
```

### Initiating a payment

You can start a new payment by creating a new order:

```python
order = client.create_order(
    {
        'merchant_order_id': 'my-custom-order-id-12345',
        'currency': 'EUR',
        'amount': 2500,  # Amount in cents
        'description': 'Purchase order 12345',
        'return_url': 'https://www.example.com',
        'transactions': [
            {
                'payment_method': 'credit-card',
            }
        ]
    }
)
```

Once you've created your order, a transaction is created and associated with it. You will need to redirect the user to
the transaction's payment URL, which you can retrieve as follows:

```python
payment_url = order['order_url']
```

It is also recommended that you store the order's ID somewhere, so you can retrieve information about it later:

```python
order_id = order['id']
```

There is a lot more data related to an order. Please refer to the API documentation provided by your PSP to learn more
about the various payment methods and options.

### Getting an order

If you want to retrieve an existing order, use the `get_order` method on the client:

```python
order = client.get_order(order_id)
```

This will return an associative array with all order information.

### Updating an order

Some fields are not read-only and you are able to update them after order has been created. You can do this using
the `update_order` method on the client:

```python
order = client.get_order(order_id)
order['description'] = 'New Order Description'
updated_order = client.update_order(order)
```

### Initiating a refund

You can refund an existing order by using the `refund_order` method on the client:

```python
refund_order = client.refund_order(order_id, {'amount': 123, 'description': 'My refund'})
```

### Capturing an order

You can initiate a capture of an order's transaction by using the `capture_order_transaction` method:

```python
client.capture_order_transaction(order_id, transaction_id)
```

### Getting the iDEAL issuers

When you create an order with the iDEAL payment method, you need to provide an issuer ID. The issuer ID is an identifier
of the bank the user has selected. You can retrieve all possible issuers by using the `get_ideal_issuers` method:

```python
issuers = client.get_ideal_issuers()
```

You can then use this information to present a list to the user of possible banks to choose from.

### Custom requests

You can send any request that the API accepts using the `send` method. E.g. instead of using the `create_order` method
you could also use the following:

```python
result = client.send(
    'POST',      # Request method
    '/orders/',  # API path
    order_data   # Data to send with the request; optional
)
```

The `$result` variable would then contain the decoded JSON returned by the API.

## Using a different CA bundle

If you need to use a different CA bundle than the one that comes with your system, you can install the Certifi package
from PyPI.

```shell script
pip install certifi
```

The certificates supplied by Certifi will be automatically used.

## Custom HTTP client

This library ships with its own minimal HTTP client for compatibility reasons. If you would like to use a different HTTP
client, you can do so by extending the `ginger_sdk.http_client.HttpClient` abstract base class and then constructing
your own client:

```python
from ginger_sdk.api_client import ApiClient

my_http_client = MyHttpClient()
client = ApiClient(my_http_client)
```

Make sure your HTTP client prefixes the endpoint URL and API version to all requests, and uses HTTP basic auth to
authenticate with the API using your API key.

## API documentation

For the complete API documentation please prefer to the resources provided by your PSP.