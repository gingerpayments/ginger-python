import unittest

from ginger_sdk import Ginger
from ginger_sdk.api_client import ApiClient


class GingerTest(unittest.TestCase):
    def test_it_creates_a_client(self) -> None:
        self.assertIsInstance(
            Ginger.create_client('https://www.example.com', 'abc123'),
            ApiClient
        )
