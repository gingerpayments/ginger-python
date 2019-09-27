from abc import ABC
from abc import abstractmethod

import requests


class HttpException(Exception):
    pass


class HttpClient(ABC):
    @abstractmethod
    def request(self, method: str, path: str, headers: dict = {}, data: str = None) -> str:
        raise NotImplementedError()


class RequestsHttpClient(HttpClient):
    _endpoint: str
    _api_key: str
    _default_headers: dict
    _default_requests_options: dict

    def __init__(self, endpoint: str, api_key: str, default_headers: dict = {},
                 default_requests_options: dict = {}) -> None:
        self._endpoint = endpoint
        self._api_key = api_key
        self._default_headers = default_headers
        self._default_requests_options = default_requests_options

    def request(self, method: str, path: str, headers: dict = {}, data: str = None) -> str:
        options: dict = {
            **self._default_requests_options,
            'auth': (self._api_key, ''),
        }

        headers = {
            **self._default_headers,
            **headers,
        }

        if data:
            options['data'] = data

        if headers:
            options['headers'] = headers

        try:
            response = requests.request(
                method=method,
                url=self._endpoint + path,
                **options
            )
        except requests.RequestException as exception:
            raise HttpException('Requests error: {}: {} ({}) for {}'.format(
                exception.errno,
                str(exception),
                'see https://requests.kennethreitz.org/en/master/api/#exceptions',
                path
            ))

        return response.text
