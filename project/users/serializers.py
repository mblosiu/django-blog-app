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
        if password is None or password == '':
            raise serializers.ValidationError({'password': 'This field is required.'})
        if len(password) < 8:
            raise serializers.ValidationError({'password': 'Passwords too short.'})

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
                    {'password': "Password should only consist uppercase letters, lowercase letters and digits"})
        if not (upper and lower and digit):
            raise serializers.ValidationError(
                {'password': "Password must contain at least 1 capital letter, 1 lowercase and 1 digit."})
        return password

    def validate_username(self, username):
        queryset = CustomUser.objects.filter(username=username)
        if queryset.exists():
            raise serializers.ValidationError({'username': 'Username {value} is taken.'})
        if username is None or username == '':
            raise serializers.ValidationError({'username': 'This field is required.'})
        return username

    def validate_email(self, email):
        queryset = CustomUser.objects.filter(email=email)
        if queryset.exists():
            raise serializers.ValidationError({'email': 'Email address {value} is taken'})
        if email is None or email == '':
            raise serializers.ValidationError({'email': 'This field is required.'})
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regex, email):
            raise serializers.ValidationError({'email': 'Email address is invalid.'})
        return email

    def create(self, validated_data):
        username = self.validated_data.get('username')
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})

        user = CustomUser(username=username, email=email)
        user.set_password(password)
        user.save()

        return user

    def update(self, user, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        password2 = validated_data.get('password2')

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})

        user.username = username
        user.email = email
        user.set_password(password)

        user.save()

        return user
