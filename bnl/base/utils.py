import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError
from ..settings import SECRET_KEY, ALGORITHM
from pymssql import connect
from pymssql.exceptions import OperationalError
from rest_framework.response import Response


def get_error_message(error) -> str:
    return error.args[0][1].decode().lower()


def get_user(token):
    try:
        user = jwt.decode(token, SECRET_KEY, ALGORITHM).get("username")
        return user
    except DecodeError or InvalidSignatureError:
        return None


def db_connect(server, username, password):
    try:
        connection = connect(server, username, password)
        cursor = connection.cursor()
        return cursor

    except OperationalError as error:
        message = get_error_message(error)
        login_error = message.count("20018") or message.count("20002")

        if login_error:
            return Response({"error": "Login failed on DB"}, 401)

        else:
            return Response({"error": "DB server not found"}, 500)
