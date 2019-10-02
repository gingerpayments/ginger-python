import platform

from .api_client import ApiClient
from .http_client import RequestsHttpClient


class Ginger(object):
    CLIENT_VERSION = '2.1.3'
    API_VERSION = 'v1'

    @staticmethod
    def create_client(endpoint: str, api_key: str, default_headers: dict = {}) -> ApiClient:
        """
        Create a new API client.
        """
        return ApiClient(
            RequestsHttpClient(
                endpoint + '/' + Ginger.API_VERSION,
                api_key,
                {
                    **default_headers,
                    **{
                        'User-Agent': 'Ginger-Python/{} ({}; Python {})'.format(
                            Ginger.CLIENT_VERSION,
                            platform.system(),
                            platform.python_version(),
                        )
                    }
                }
            )
        )
