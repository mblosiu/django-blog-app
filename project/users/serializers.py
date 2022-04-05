import re

from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, password):
        if password != self.initial_data.get('password2'):
            raise serializers.ValidationError("Passwords must match.")
        if len(password) < 8:
            raise serializers.ValidationError('Passwords too short.')

        upper = False
        lower = False
        digit = False

        for character in password:
            if character.isupper():
                upper = True
            if character.islower():
                lower = True
            if character.isdigit():
                digit = True
            if not (character.isupper() or character.islower() or character.isdigit()):
                raise serializers.ValidationError(
                    "Password should only consist uppercase letters, lowercase letters and digits")
        if not (upper and lower and digit):
            raise serializers.ValidationError(
                "Password must contain at least 1 capital letter, 1 lowercase and 1 digit.")
        return password

    def create(self, validated_data):
        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')

        user = CustomUser(username=username, email=email)
        user.set_password(password)
        user.save()

        return user

    def update(self, user, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        user.username = username
        user.email = email
        user.set_password(password)

        user.save()

        return user
