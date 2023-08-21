from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions


from users.models import User
from foodgram.settings import MAX_LENGTH, EMAIL_MAX_LENGTH
from app.serializers import RecipeSerializer


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z', max_length=MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())])
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "is_subscribed"
        )
        model = User

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            return current_user.subscriber.filter(author=obj).exists()
        return False


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z',
                                      required=True, max_length=MAX_LENGTH)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        read_only_fields = ('id', )

    def validate_username(self, value):
        if (
            value.lower() == 'me'
        ):
            raise serializers.ValidationError(
                'Нельзя указывать me в качестве имени')
        return value


class SetPasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('new_password', 'current_password')

    def validate(self, attrs):
        user = self.context['request'].user
        password = attrs.get("current_password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs


class AuthorSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "is_subscribed", "recipes", "recipes_count"
        )

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].query_params['recipes_limit']
        return RecipeSerializer(obj.recipes[:recipes_limit], many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            return current_user.subscriber.filter(author=obj).exists()
        return False
