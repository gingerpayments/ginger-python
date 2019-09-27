import json
import unittest

from unittest import mock

from ginger_sdk.api_client import ApiClient
from ginger_sdk.api_client import HttpRequestError
from ginger_sdk.api_client import ServerError
from ginger_sdk.http_client import HttpClient


class ApiClientTest(unittest.TestCase):
    _http_client: HttpClient
    _api_client: ApiClient

    def setUp(self) -> None:
        self._http_client = mock.MagicMock()
        self._api_client = ApiClient(self._http_client)

    def test_it_gets_ideal_issuers(self) -> None:
        expected_issuers = [
            {
                'id': 'INGBNL2A',
                'list_type': 'Deutschland',
                'name': 'Issuer Simulation V3 - ING',
            },
            {
                'id': 'RABONL2U',
                'list_type': 'Deutschland',
                'name': 'Issuer Simulation V3 - RABO',
            },
        ]
        self._http_client.request.return_value = json.dumps(expected_issuers)

        issuers = self._api_client.get_ideal_issuers()

        self._http_client.request.assert_called_with('GET', '/ideal/issuers/')
        self.assertEqual(expected_issuers, issuers)

    def test_it_gets_an_order(self) -> None:
        expected_order = {
            'id': 'fcbfdd3a-ea2c-4240-96b2-613d49b79a55',
            'transactions': [
                {
                    'id': 'ddc76c84-3fc2-4a16-85b9-a895f6bdc696',
                    'amount': 995,
                },
            ],
        }
        self._http_client.request.return_value = json.dumps(expected_order)

        order = self._api_client.get_order('fcbfdd3a-ea2c-4240-96b2-613d49b79a55')

        self._http_client.request.assert_called_with('GET', '/orders/fcbfdd3a-ea2c-4240-96b2-613d49b79a55/')
        self.assertEqual(expected_order, order)

    def test_it_creates_an_order(self) -> None:
        expected_order = {
            'amount': 995,
            'currency': 'EUR',
            'description': 'My amazing order',
            'merchant_order_id': 'my-custom-id-7131b462',
            'return_url': 'https://www.example.com',
            'webhook_url': 'https://www.example.com/hook',
            'customer': {'first_name': 'John', 'last_name': 'Doe'},
            'extra': {'my-custom-data': 'Foobar'},
            'transactions': [
                {
                    'payment_method': 'ideal',
                    'payment_method_details': {'issuer_id': 'INGBNL2A'},
                    'expiration_period': 'PT10M',
                },
            ],
        }
        self._http_client.request.return_value = json.dumps(expected_order)

        order = self._api_client.create_order(expected_order)

        self._http_client.request.assert_called_with(
            'POST',
            '/orders/',
            {'Content-Type': 'application/json'},
            json.dumps(expected_order)
        )
        self.assertEqual(expected_order, order)

    def test_it_updates_an_order(self) -> None:
        expected_order = {
            'id': 'fcbfdd3a-ea2c-4240-96b2-613d49b79a55',
            'amount': 995,
            'currency': 'EUR',
            'description': 'My amazing order',
            'merchant_order_id': 'my-custom-id-7131b462',
            'return_url': 'https://www.example.com',
            'webhook_url': 'https://www.example.com/hook',
            'customer': {'first_name': 'John', 'last_name': 'Doe'},
            'extra': {'my-custom-data': 'Foobar'},
            'transactions': [
                {
                    'payment_method': 'ideal',
                    'payment_method_details': {'issuer_id': 'INGBNL2A'},
                    'expiration_period': 'PT10M',
                },
            ],
        }
        self._http_client.request.return_value = json.dumps(expected_order)

        order = self._api_client.update_order(
            'fcbfdd3a-ea2c-4240-96b2-613d49b79a55',
            {'description': 'My new description'}
        )

        self._http_client.request.assert_called_with(
            'PUT',
            '/orders/fcbfdd3a-ea2c-4240-96b2-613d49b79a55/',
            {'Content-Type': 'application/json'},
            json.dumps({'description': 'My new description'})
        )
        self.assertEqual(expected_order, order)

    def test_it_refunds_an_order(self) -> None:
        expected_order = {
            'id': 'fcbfdd3a-ea2c-4240-96b2-613d49b79a55',
            'transactions': [
                {
                    'id': 'ddc76c84-3fc2-4a16-85b9-a895f6bdc696',
                    'amount': 995,
                }
            ]
        }
        self._http_client.request.return_value = json.dumps(expected_order)

        order = self._api_client.refund_order(
            'fcbfdd3a-ea2c-4240-96b2-613d49b79a55',
            {'amount': 123, 'description': 'My refund'}
        )

        self._http_client.request.assert_called_with(
            'POST',
            '/orders/fcbfdd3a-ea2c-4240-96b2-613d49b79a55/refunds/',
            {'Content-Type': 'application/json'},
            json.dumps({'amount': 123, 'description': 'My refund'})
        )
        self.assertEqual(expected_order, order)

    def test_it_throws_an_exception_on_http_client_error(self) -> None:
        self._http_client.request.side_effect = HttpRequestError('Whoops!')

        with self.assertRaises(HttpRequestError):
            self._api_client.get_ideal_issuers()

    def test_it_throws_an_exception_on_json_decode_error(self) -> None:
        self._http_client.request.return_value = 'definitely not json'

        with self.assertRaises(json.JSONDecodeError):
            self._api_client.get_ideal_issuers()

    def test_it_throws_an_exception_on_server_error(self) -> None:
        self._http_client.request.return_value = json.dumps(
            {'error': {'status': '503', 'type': 'ConnectionError', 'value': 'The server made a boo-boo'}}
        )

        with self.assertRaises(ServerError):
            self._api_client.get_ideal_issuers()
