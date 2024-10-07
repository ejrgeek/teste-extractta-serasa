from rest_framework import serializers
from apps.authentication.models import Login


class LoginEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login()
        fields = ["email", "password"]

        extra_kwargs = {"password": {"write_only": True}}
