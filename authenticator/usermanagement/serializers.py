from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    CustomUserSerializer
    """
    class Meta:
        """
        Meta
        """
        model = CustomUser
        fields = "__all__"
