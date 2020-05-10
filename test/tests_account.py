import unittest
import requests
import json

from application.controllers import account_controller

account1 = {"login": "test", "password": "test", "question": "Jaki masz login?", "answer": "test"}
account2 = {"login": "test123", "password": "123", "question": "Jaki masz login?", "answer": "test"}
server_address = 'http://0.0.0.0:2137'


class TestLogin(unittest.TestCase):

    def test_login_positive(self):
        request_result = requests.post(url=server_address + '/login', data=json.dumps(account1))
        print(json.loads(request_result.content))

        assert request_result.status_code == 200

    def test_login_negative_authFail(self):
        request_result = requests.post(url=server_address + '/login', data=json.dumps(account2))
        print(json.loads(request_result.content))

        assert request_result.status_code == 401


class TestRegister(unittest.TestCase):
    account_missing_argument = {"login": account2["login"] + "abc", "password": account2["password"],
                                "question": account2["question"]}

    # def test_register_positive(self):
    #     request_result = requests.post(url=server_address + '/register', data=json.dumps(account2))
    #
    #     print(json.loads(request_result.content))
    #
    #     assert request_result.status_code == 201
    #
    #     session = Session()
    #     account_found = account_controller.account_get(account2["login"])
    #     assert account_found is not None
    #     session.delete(account_found)
    #     session.commit()
    #     session.close()

    def test_register_negative_existingaccount(self):
        request_result = requests.post(url=server_address + '/register', data=json.dumps(account1))
        print(json.loads(request_result.content))

        assert request_result.status_code == 406

    def test_register_negative_missingArgument(self):
        request_result = requests.post(url=server_address + '/register',
                                       data=json.dumps(self.account_missing_argument))
        print(json.loads(request_result.content))

        assert request_result.status_code == 400

        found_user = account_controller.account_get(self.account_missing_argument["login"])

        assert found_user is None


class TestForgetPassword(unittest.TestCase):
    account1 = {"login": account1["login"]}
    first_invalid_account_data = json.dumps({"login": "test123"})
    second_invalid_account_data = json.dumps({"login": "test123", "answer": "test"})

    def test_remind_password_positive(self):
        request_result = requests.post(url=server_address + '/account/remind_password',
                                       data=json.dumps({"login": self.account1["login"]}))
        data = json.loads(request_result.content)
        print(json.loads(request_result.content))

        assert "question" in data.keys()
        assert request_result.status_code == 200

        request_result = requests.post(url=server_address + '/account/remind_password',
                                       data=json.dumps({"login": account1["login"],
                                                        "answer": account1["answer"]}))
        data = json.loads(request_result.content)
        print(json.loads(request_result.content))

        assert "actual_password" in data.keys()
        assert request_result.status_code == 200


class TestChangeQuestionAnsweraccount(unittest.TestCase):
    account_missing_argument = {"login": account1["login"], "password": account1["password"],
                                "answer": account1["answer"]}

    def test_update_question_or_answer_positive(self):
        request_result = requests.put(url=server_address + '/account/change_question_answer',
                                      data=json.dumps(
                                          {"login": account1["login"], "password": account1["password"],
                                           "question": "Jak ci mija dzień?", "answer": "dobrze"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200

        request_result = requests.put(url=server_address + '/account/change_question_answer',
                                      data=json.dumps(
                                          {"login": account1["login"], "password": account1["password"],
                                           "question": account1["question"], "answer": account1["answer"]}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200

    def test_update_question_or_answer_negative_missingArgument(self):
        request_result = requests.put(url=server_address + '/account/change_question_answer',
                                      data=json.dumps(self.account_missing_argument))
        print(json.loads(request_result.content))
        assert request_result.status_code == 400


class TestDeleteaccount(unittest.TestCase):
    def test_delete_positive(self):
        request_result = requests.delete(url=server_address + '/account/delete', data=json.dumps(account1))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200

    def test_delete_negative_missingArgument(self):
        request_result = requests.delete(url=server_address + '/account/delete',
                                         data=json.dumps({"login": "magda"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 400


class TestChangePassword(unittest.TestCase):
    def test_change_password_positive(self):
        request_result = requests.put(url=server_address + '/account/change_password',
                                      data=json.dumps(
                                          {"login": account1["login"], "password": account1["password"],
                                           "new_password": "12345"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200
        requests.put(url=server_address + '/account/change_password',
                     data=json.dumps(
                         {"login": account1["login"], "password": "12345",
                          "new_password": "test"}))

    def test_change_password_negative(self):
        request_result = requests.put(url=server_address + '/account/change_password',
                                      data=json.dumps(
                                          {"login": account1["login"], "password": account1["password"] + "123",
                                           "new_password": "12345"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 401


class TestAdminModifyaccount(unittest.TestCase):

    def test_account_admin_modify_account_positive(self):
        request_result = requests.put(url=server_address + '/account/admin/modify_account',
                                      data=json.dumps(
                                          {"login": account1["login"], "password": account1["password"],
                                           "account_login": "magda", "account_password": "1234567",
                                           "account_question": "jak pan jezus powiedział",
                                           "account_answer": "tak jak pan jezus powiedział"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200

        request_result = requests.put(url=server_address + '/account/admin/modify_account',
                                      data=json.dumps(
                                          {"login": account1["login"], "password": account1["password"],
                                           "account_login": "magda", "account_password": "gessler",
                                           "account_question": "jak pan jezus powiedział",
                                           "account_answer": "tak jak pan jezus powiedział"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200

    def test_account_admin_modify_account_negative(self):
        request_result = requests.put(url=server_address + '/account/admin/modify_account',  # unauthorized
                                      data=json.dumps(
                                          {"login": account1["login"], "password": account1["password"] + "123",
                                           "account_login": "magda", "account_password": "gessler",
                                           "account_question": "jak pan jezus powiedział",
                                           "account_answer": "tak jak pan jezus powiedział"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 401

        request_result = requests.put(url=server_address + '/account/admin/modify_account',  # account is not admin
                                      data=json.dumps(
                                          {"login": "magda", "password": "gessler",
                                           "account_login": "magda", "account_password": "gessler",
                                           "account_question": "jak pan jezus powiedział",
                                           "account_answer": "tak jak pan jezus powiedział"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 403


if __name__ == '__main__':
    unittest.main()
