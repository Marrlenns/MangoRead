from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for creating a new User."""
    image = serializers.ImageField(default='avatarki/default.png')
    username = serializers.CharField(max_length=50)
    nickname = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = 'image username nickname password'.split()

    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise ValidationError("This username is already in use!!!")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)

        user.save()

        Token.objects.create(user=user)

        return user


class LoginSerializer(serializers.ModelSerializer):
    """Serializer for User authentication."""
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"},
        validators=[validate_password], required=True
    )

    class Meta:
        model = User
        fields = "id username nickname password".split()
        read_only_fields = "id nickname".split()


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the user profile."""
    class Meta:
        model = User
        fields = "image username nickname".split()

    def validate(self, attrs):
        queryset = User.objects.exclude(id=self.context["request"].user.id)
        if queryset.filter(username=attrs["username"]).exists():
            raise ValidationError({"message": "Username already in use!"})
        return attrs


class UpdatePasswordSerializer(LoginSerializer):
    """Serializer for changing a user's password."""
    old_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = "old_password password password2".split()