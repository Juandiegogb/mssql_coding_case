from rest_framework.serializers import Serializer, CharField, IntegerField


class LoginSerializer(Serializer):
    username = CharField()
    password = CharField()


class PayrollSerializer(Serializer):
    token = CharField(required=True)
    year = IntegerField(required=False, default="NULL")
    month = IntegerField(required=False, default="NULL")
