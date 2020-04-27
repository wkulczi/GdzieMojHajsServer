import sqlalchemy
from sqlalchemy import update

from application import db_model


def user_authorize(data: dict):
    if not all(elem in data.keys() for elem in ["login", "password"]):
        raise ServerLogicException("Missing parameters!")

    session = db_model.Session()
    found_user = session.query(db_model.Uzytkownik).filter_by(login=data["login"], password=data["password"]).first()
    session.close()

    return found_user is not None


def user_exists(login: str):
    session = db_model.Session()
    found_user = session.query(db_model.Uzytkownik).filter_by(login=login).first()
    session.close()

    return found_user is not None


def user_get(login: str) -> db_model.Uzytkownik:
    session = db_model.Session()

    found_user = session.query(db_model.Uzytkownik).filter_by(login=login).first()
    session.close()

    if found_user is None:
        raise ServerLogicException("User not found!")
    else:
        return found_user


def user_insert_to_db(data: dict):
    if not all(elem in data.keys() for elem in ["login", "password", "question", "answer"]):
        raise ServerLogicException("Missing parameters!")
    if user_exists(data["login"]):
        raise ServerLogicException("User already exists!")

    session = db_model.Session()

    user_to_insert = db_model.Uzytkownik(login=data["login"], password=data["password"],
                                         question=data["question"], answer=data["answer"], role="user")
    session.add(user_to_insert)
    session.commit()
    session.close()

    inserted_user = user_get(data["login"])

    return inserted_user


def user_change_password(data: dict):
    session = db_model.Session()

    if not all(elem in data.keys() for elem in ["login", "new_password"]):
        raise ServerLogicException("Missing Arguments!")

    session.query(db_model.Uzytkownik).filter_by(login=data["login"]).update({"password": data["new_password"]})
    session.commit()
    session.close()

    modified_user = user_get(data["login"])

    if modified_user.password != data["new_password"]:
        raise ServerLogicException("Failed to modify in database!")


def user_change_question_answer(data: dict):
    session = db_model.Session()

    if not all(elem in data.keys() for elem in ["login", "question", "answer"]):
        raise ServerLogicException("Missing Arguments!")

    session.query(db_model.Uzytkownik).filter_by(login=data["login"]).update(
        {"question": data["question"],
         "answer": data["answer"]})
    session.commit()
    session.close()

    modified_user = user_get(data["login"])
    print(modified_user)

    if modified_user.question != data["question"] or modified_user.answer != data["answer"]:
        raise ServerLogicException("Failed to modify in database!")


def user_admin_modify(data: dict):
    if not ("user_login" in data.keys() or any(elem in data.keys() for elem in
                                               ["user_password", "user_role", ["user_question", "user_answer"]])):
        raise ServerLogicException("Missing Arguments!")

    renamed_dict = {}

    for key in data.keys():
        renamed_dict.update({key.replace("user_", ""): data[key]})

    session = db_model.Session()
    session.query(db_model.Uzytkownik).filter_by(login=renamed_dict["login"]).update(renamed_dict)
    session.commit()
    session.close()


def user_delete(login: str):
    # TODO:Fix cascade updating and deleting
    session = db_model.Session()

    # session.delete(user_get(login)).first()
    # session.delete(db_model.Uzytkownik).where(login=login)
    session.query(db_model.Uzytkownik).filter_by(login=login).delete()

    session.commit()
    session.close()

    if user_exists(login):
        raise ServerLogicException("Failed to delete user from database!")


def user_validate_answer(data: dict):
    if not user_exists(data["login"]):
        raise ServerLogicException("User with given login not exists!")

    elif not all(elem in data.keys() for elem in ["login", "answer"]):
        raise ServerLogicException("Missing Arguments!")

    user = user_get(data["login"])

    if user.answer != data["answer"]:
        raise ServerLogicException("Wrong answer!")
    else:
        return user.password


class ServerLogicException(Exception):
    pass
