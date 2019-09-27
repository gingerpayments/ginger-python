import json

from .http_client import HttpClient


class HttpRequestError(Exception):
    def __init__(self, exception) -> None:
        self.message = 'An error occurred while processing the request: {}'.format(str(exception))


class ServerError(Exception):
    @classmethod
    def from_result(cls, result: dict) -> 'ServerError':
        return cls('{}({}): {}'.format(
            result['error'].get('type'),
            result['error'].get('status'),
            result['error'].get('value'),
        ))


class ApiClient(object):
    _http_client: HttpClient

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def get_ideal_issuers(self) -> list:
        """
        Get a list of possible iDEAL issuers.

        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        try:
            response = self._http_client.request('GET', '/ideal/issuers/')
        except Exception as exception:
            raise HttpRequestError(exception) from exception

        return self._interpret_response(response)

    def get_order(self, id: str) -> dict:
        """
        Get an order.

        :param str id: The order ID.
        :return: The order.
        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        try:
            response = self._http_client.request('GET', '/orders/{}/'.format(id))
        except Exception as exception:
            raise HttpRequestError(exception) from exception

        return self._interpret_response(response)

    def create_order(self, order_data: dict) -> dict:
        """
        Create a new order.

        :param dict order_data: Dictionary with attributes and values to create.
        :return: The newly created order.
        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        try:
            response = self._http_client.request(
                'POST',
                '/orders/',
                {'Content-Type': 'application/json'},
                json.dumps(order_data),
            )
        except Exception as exception:
            raise HttpRequestError(exception) from exception

        return self._interpret_response(response)

    def update_order(self, id: str, order_data: dict) -> dict:
        """
        Update an order.

        :param str id: The ID of the order to update.
        :param dict order_data: Dictionary with attributes and values to update.
        :return: The newly updated order.
        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        try:
            response = self._http_client.request(
                'PUT',
                '/orders/{}/'.format(id),
                {'Content-Type': 'application/json'},
                json.dumps(order_data),
            )
        except Exception as exception:
            raise HttpRequestError(exception) from exception

        return self._interpret_response(response)

    def refund_order(self, id: str, order_data: dict) -> dict:
        """
        Refund an order.

        :param str id: The ID of the order to refund.
        :param dict order_data: Refund data.
        :return: The newly created refund.
        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        try:
            response = self._http_client.request(
                'POST',
                '/orders/{}/refunds/'.format(id),
                {'Content-Type': 'application/json'},
                json.dumps(order_data),
            )
        except Exception as exception:
            raise HttpRequestError(exception) from exception

        return self._interpret_response(response)

    @staticmethod
    def _interpret_response(response: str) -> dict:
        """
        :raises HttpRequestError:
        :raises json.JSONDecodeError:
        """
        result = json.loads(response)

        if 'error' in result:
            raise ServerError.from_result(result)

        return result
