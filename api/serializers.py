from rest_framework import serializers
from api.models import User

class UserApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined"
        ]
