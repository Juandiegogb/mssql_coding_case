import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from pymssql import connect
from pymssql.exceptions import OperationalError
from time import time_ns
from ..settings import (
    SECRET_KEY,
    ALGORITHM,
    server_db,
    user_db,
    password_db,
    database_name,
)
from .serializers import LoginSerializer, PayrollSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .utils import get_user


@extend_schema(request=LoginSerializer, responses={200: dict})
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": "Username and password are required"}, 400)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        server = "localhost"

        payload = {"username": username, "created_at": time_ns()}
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

        try:
            connect(server, username, password)

        except OperationalError:
            return Response({"error": "Login failled, invalid credentials"}, 401)

        return Response({"token": token}, 200)


@extend_schema(
    request=PayrollSerializer,
    responses={200: dict},
    parameters=[
        OpenApiParameter("token", OpenApiTypes.STR),
        OpenApiParameter("month", OpenApiTypes.INT),
        OpenApiParameter("year", OpenApiTypes.INT),
    ],
)
class PayrollView(APIView):
    def get(self, request, *args, **kwargs):
        area = self.kwargs.get("area")
        serializer = PayrollSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response({"error": "Token parameter is required"}, 400)
        token = serializer.validated_data["token"]

        user = get_user(token)
        if not user:
            return Response({"error": "Invalid token"}, 401)

        try:
            connection = connect(server_db, user_db, password_db, database_name)

        except OperationalError:
            return Response({"error": "Login failled, invalid credentials"}, 401)

        cursor = connection.cursor()

        if area:
            match area:
                case "IT":
                    query = f"execute as user = '{user}'; select * from itpayroll"

                case "Logistics":
                    query = (
                        f"execute as user = '{user}'; select * from Logisticspayroll"
                    )

                case "HR":
                    query = f"execute as user = '{user}'; select * from Hrpayroll"

                case _:
                    result = "invalid area"

        else:
            query = f"execute as user = '{user}'; select * from payments"

        try:
            if query:
                cursor.execute(query)
                result = cursor.fetchall()

        except OperationalError:
            return Response({"error": "Denied access"}, 401)
        return Response(result, 200)
