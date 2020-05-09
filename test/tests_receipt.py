import unittest
import requests
import json

from application import db_model

user_valid = {"login": "test", "password": "test"}
user_invalid = {"login": "test123", "password": "123"}
server_address = 'http://0.0.0.0:2137'


class TestUserGetReceipts(unittest.TestCase):

    def test_get_receipts_positive(self):
        request_result = requests.get(
            url=server_address + f'/receipts?login={user_valid["login"]}&password={user_valid["password"]}')
        print(json.loads(request_result.content))

        assert request_result.status_code == 200

    def test_get_receipts_authFail(self):
        request_result = requests.get(
            url=server_address + f'/receipts?login={user_invalid["login"]}&password={user_invalid["password"]}')
        print(json.loads(request_result.content))

        assert request_result.status_code == 401


if __name__ == '__main__':
    unittest.main()
