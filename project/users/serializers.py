from math import floor

from rest_framework import serializers
from django.utils.timezone import now

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    user_age = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'password2', 'name', 'surname', 'birth_date', 'user_age']
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

    def update(self, instance, validated_data):
        email = validated_data.get('email') or None
        password = validated_data.get('password')
        password2 = validated_data.get('password2')
        name = validated_data.get('name')
        surname = validated_data.get('surname')
        birth_date = validated_data.get('birth_date')

        if email:
            instance.email = email
        if password and password2:
            instance.set_password(password)
        if name:
            instance.name = name
        if surname:
            instance.surname = surname
        if birth_date:
            instance.birth_date = birth_date

        instance.save()

        return instance

    def get_user_age(self, obj):
        if obj.birth_date:
            timedelta = now() - obj.birth_date
            return floor(timedelta.days / 365.25)
        else:
            return None
