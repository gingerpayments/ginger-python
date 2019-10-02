import json
import unittest

from unittest import mock

import requests

from ginger_sdk.http_client import HttpClient
from ginger_sdk.http_client import HttpException
from ginger_sdk.http_client import RequestsHttpClient


class RequestsHttpClientTest(unittest.TestCase):
    _client: HttpClient
    _request_mock: mock.MagicMock

    def setUp(self) -> None:
        self._client = RequestsHttpClient(
            'https://www.example.com',
            '1a1b2e63c55e',
        )

        patcher = mock.patch('ginger_sdk.http_client.requests.request')
        self._request_mock = patcher.start()
        self.addCleanup(patcher.stop)

        def side_effect(*_, **kwargs):
            response_mock = mock.MagicMock()

            if kwargs['url'] == 'https://www.example.com/empty/response':
                response_mock.text = None
            else:
                response_mock.text = json.dumps(kwargs)

            return response_mock

        self._request_mock.side_effect = side_effect

    def test_it_sends_a_request(self) -> None:
        response = self._client.request(
            'POST',
            '/foo/bar',
            {'Content-Type': 'text/plain'},
            'request data'
        )

        self.assertEqual(
            {
                'url': 'https://www.example.com/foo/bar',
                'method': 'POST',
                'data': 'request data',
                'headers': {'Content-Type': 'text/plain'},
                'auth': ['1a1b2e63c55e', ''],
            },
            json.loads(response)
        )

    def test_it_sets_default_headers(self) -> None:
        client = RequestsHttpClient(
            'https://www.example.com',
            '1a1b2e63c55e',
            {'X-Custom-Header': 'foobar'},
        )

        response = client.request('GET', '/foo/bar')

        self.assertEqual(
            {
                'url': 'https://www.example.com/foo/bar',
                'method': 'GET',
                'auth': ['1a1b2e63c55e', ''],
                'headers': {'X-Custom-Header': 'foobar'},
            },
            json.loads(response)
        )

    def test_it_sets_custom_options(self) -> None:
        client = RequestsHttpClient(
            'https://www.example.com',
            '1a1b2e63c55e',
            {},
            {'cert': '/my/clientcert.crt'},
        )

        response = client.request('GET', '/foo/bar')

        self.assertEqual(
            {
                'url': 'https://www.example.com/foo/bar',
                'method': 'GET',
                'auth': ['1a1b2e63c55e', ''],
                'cert': '/my/clientcert.crt',
            },
            json.loads(response)
        )

    def test_it_returns_none_on_empty_response_body(self) -> None:
        response = self._client.request('POST', '/empty/response')

        self.assertIsNone(response)

    def test_it_raises_an_exception_on_requests_error(self) -> None:
        self._request_mock.side_effect = requests.TooManyRedirects('Exceeded 10 redirects.')

        with self.assertRaises(HttpException) as exception_ctx:
            self._client.request('GET', '/error')

        self.assertEqual(
            'Requests error: None: Exceeded 10 redirects. '
            '(see https://requests.kennethreitz.org/en/master/api/#exceptions) for /error',
            str(exception_ctx.exception)
        )
