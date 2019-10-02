import json

from typing import Optional
from typing import Union

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
        return self.send('GET', '/ideal/issuers/')

    def get_order(self, id: str) -> dict:
        """
        Get an order.

        :param str id: The order ID.
        :return: The order.
        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        return self.send('GET', '/orders/{}/'.format(id))

    def create_order(self, order_data: dict) -> dict:
        """
        Create a new order.

        :param dict order_data: Dictionary with attributes and values to create.
        :return: The newly created order.
        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        return self.send('POST', '/orders/', order_data)

    def update_order(self, id: str, order_data: dict) -> dict:
        """
        Update an order.

        :param str id: The ID of the order to update.
        :param dict order_data: Dictionary with attributes and values to update.
        :return: The newly updated order.
        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        return self.send('PUT', '/orders/{}/'.format(id), order_data)

    def refund_order(self, id: str, order_data: dict) -> dict:
        """
        Refund an order.

        :param str id: The ID of the order to refund.
        :param dict order_data: Refund data.
        :return: The newly created refund.
        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        return self.send('POST', '/orders/{}/refunds/'.format(id), order_data)

    def capture_order_transaction(self, order_id: str, transaction_id: str) -> None:
        """
        Capture an order transaction.

        :param str order_id: The ID of the order.
        :param str transaction_id: The ID of the transaction to capture.
        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        self.send('POST', '/orders/{}/transactions/{}/captures/'.format(order_id, transaction_id))

    def send(self, method: str, path: str, data: dict = None) -> Union[dict, list, None]:
        """
        Send a request to the API.

        :param str method: HTTP request method
        :param str path: URL path to call
        :param str data: Request data to send
        :raises HttpRequestError: When an error occurred while processing the request.
        :raises json.JSONDecodeError: When the response data could not be decoded.
        """
        try:
            response = self._http_client.request(
                method,
                path,
                {'Content-Type': 'application/json'} if data else {},
                json.dumps(data) if data else None
            )
        except Exception as exception:
            raise HttpRequestError(exception) from exception

        return self._interpret_response(response)

    @staticmethod
    def _interpret_response(response: Optional[str]) -> Optional[dict]:
        """
        :raises HttpRequestError:
        :raises json.JSONDecodeError:
        """
        if not response:
            return None

        result = json.loads(response)

        if 'error' in result:
            raise ServerError.from_result(result)

        return result
