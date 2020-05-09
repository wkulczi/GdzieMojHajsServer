import unittest
import requests
import json

from application import db_model

user_valid = {"login": "test", "password": "test", "question": "Jaki masz login?", "answer": "test"}
user_invalid = {"login": "test123", "password": "123", "question": "Jaki masz login?", "answer": "test"}
server_address = 'http://0.0.0.0:2137'


class TestLogin(unittest.TestCase):

    def test_login_positive(self):
        # positive case
        request_result = requests.post(url=server_address + '/login', data=json.dumps(user_valid))
        print(json.loads(request_result.content))

        assert request_result.status_code == 200

    def test_login_negative_authFail(self):
        # negative case
        request_result = requests.post(url=server_address + '/login', data=json.dumps(user_invalid))
        print(json.loads(request_result.content))

        assert request_result.status_code == 401


class TestRegister(unittest.TestCase):
    user_missing_argument = {"login": user_invalid["login"] + "abc", "password": user_invalid["password"],
                             "question": user_invalid["question"]}

    def test_register_positive(self):
        request_result = requests.post(url=server_address + '/register', data=json.dumps(user_invalid))

        print(json.loads(request_result.content))

        assert request_result.status_code == 201

        session = db_model.Session()
        user_found = session.query(db_model.User).filter_by(login=user_invalid["login"],
                                                            password=user_invalid["password"],
                                                            question=user_invalid["question"],
                                                            answer=user_invalid["answer"]).first()
        assert user_found is not None
        session.delete(user_found)
        session.commit()
        session.close()

    def test_register_negative_existingUser(self):
        request_result = requests.post(url=server_address + '/register', data=json.dumps(user_valid))
        print(json.loads(request_result.content))

        assert request_result.status_code == 406

        session = db_model.Session()
        user_found = session.query(db_model.User).filter_by(login=user_valid["login"],
                                                            password=user_valid["password"],
                                                            question=user_valid["question"],
                                                            answer=user_valid["answer"]).first()
        session.close()

    def test_register_negative_missingArgument(self):
        request_result = requests.post(url=server_address + '/register',
                                       data=json.dumps(self.user_missing_argument))
        print(json.loads(request_result.content))

        assert request_result.status_code == 400

        session = db_model.Session()
        user_found = session.query(db_model.User).filter_by(
            login=self.user_missing_argument["login"],
            password=self.user_missing_argument["password"],
            question=self.user_missing_argument["question"]).first()
        session.close()

        assert user_found is None


class TestForgetPassword(unittest.TestCase):
    user_valid = {"login": user_valid["login"]}
    first_invalid_account_data = json.dumps({"login": "test123"})
    second_invalid_account_data = json.dumps({"login": "test123", "answer": "test"})

    def test_remind_password_positive(self):
        request_result = requests.post(url=server_address + '/user/remind_password',
                                       data=json.dumps({"login": self.user_valid["login"]}))
        data = json.loads(request_result.content)
        print(json.loads(request_result.content))

        assert "question" in data.keys()
        assert request_result.status_code == 200

        request_result = requests.post(url=server_address + '/user/remind_password',
                                       data=json.dumps({"login": user_valid["login"],
                                                        "answer": user_valid["answer"]}))
        data = json.loads(request_result.content)
        print(json.loads(request_result.content))

        assert "actual_password" in data.keys()
        assert request_result.status_code == 200


class TestChangeQuestionAnswerUser(unittest.TestCase):
    user_missing_argument = {"login": user_valid["login"], "password": user_valid["password"],
                             "answer": user_valid["answer"]}

    def test_update_question_or_answer_positive(self):
        request_result = requests.put(url=server_address + '/user/change_question_answer',
                                      data=json.dumps(
                                          {"login": user_valid["login"], "password": user_valid["password"],
                                           "question": "Jak ci mija dzień?", "answer": "dobrze"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200

        request_result = requests.put(url=server_address + '/user/change_question_answer',
                                      data=json.dumps(
                                          {"login": user_valid["login"], "password": user_valid["password"],
                                           "question": user_valid["question"], "answer": user_valid["answer"]}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200

    def test_update_question_or_answer_negative_missingArgument(self):
        request_result = requests.put(url=server_address + '/user/change_question_answer',
                                      data=json.dumps(self.user_missing_argument))
        print(json.loads(request_result.content))
        assert request_result.status_code == 400


class TestDeleteUser(unittest.TestCase):
    def test_delete_positive(self):
        request_result = requests.delete(url=server_address + '/user/delete', data=json.dumps(user_valid))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200

    def test_delete_negative_missingArgument(self):
        request_result = requests.delete(url=server_address + '/user/delete',
                                         data=json.dumps({"login":"magda"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 400


class TestChangePassword(unittest.TestCase):
    def test_change_password_positive(self):
        request_result = requests.put(url=server_address + '/user/change_password',
                                      data=json.dumps(
                                          {"login": user_valid["login"], "password": user_valid["password"],
                                           "new_password": "12345"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200
        requests.put(url=server_address + '/user/change_password',
                     data=json.dumps(
                         {"login": user_valid["login"], "password": "12345",
                          "new_password": "test"}))

    def test_change_password_negative(self):
        request_result = requests.put(url=server_address + '/user/change_password',
                                      data=json.dumps(
                                          {"login": user_valid["login"], "password": user_valid["password"] + "123",
                                           "new_password": "12345"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 401


class TestAdminModifyUser(unittest.TestCase):

    def test_user_admin_modify_user_positive(self):
        request_result = requests.put(url=server_address + '/user/admin/modify_user',
                                      data=json.dumps(
                                          {"login": user_valid["login"], "password": user_valid["password"],
                                           "user_login": "magda", "user_password": "1234567",
                                           "user_question": "jak pan jezus powiedział",
                                           "user_answer": "tak jak pan jezus powiedział"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200

        request_result = requests.put(url=server_address + '/user/admin/modify_user',
                                      data=json.dumps(
                                          {"login": user_valid["login"], "password": user_valid["password"],
                                           "user_login": "magda", "user_password":"gessler",
                                           "user_question": "jak pan jezus powiedział",
                                           "user_answer": "tak jak pan jezus powiedział"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 200

    def test_user_admin_modify_user_negative(self):
        request_result = requests.put(url=server_address + '/user/admin/modify_user',  # unauthorized
                                      data=json.dumps(
                                          {"login": user_valid["login"], "password": user_valid["password"] + "123",
                                           "user_login": "magda", "user_password": "gessler",
                                           "user_question": "jak pan jezus powiedział",
                                           "user_answer": "tak jak pan jezus powiedział"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 401

        request_result = requests.put(url=server_address + '/user/admin/modify_user',  # user is not admin
                                      data=json.dumps(
                                          {"login": "magda", "password": "gessler",
                                           "user_login": "magda", "user_password": "gessler",
                                           "user_question": "jak pan jezus powiedział",
                                           "user_answer": "tak jak pan jezus powiedział"}))
        print(json.loads(request_result.content))
        assert request_result.status_code == 403


if __name__ == '__main__':
    unittest.main()
