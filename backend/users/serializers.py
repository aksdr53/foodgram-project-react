from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueValidator


from users.models import User
from api_yamdb.settings import MAX_LENGTH, EMAIL_MAX_LENGTH


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z', max_length=MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )
        model = User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z',
                                      required=True, max_length=MAX_LENGTH)

    def validate_username(self, value):
        if (
            value.lower() == 'me'
        ):
            raise serializers.ValidationError(
                'Нельзя указывать me в качестве имени')
        return value


class ProfileSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class TokenSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        if not User.objects.filter(username=username).exists():
            raise NotFound("Данный пользователь не зарегистрирован")
        return data
