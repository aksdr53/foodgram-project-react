import base64

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.core.files.base import ContentFile


from app.models import Recipe
from users.models import User
from foodgram.settings import MAX_LENGTH, EMAIL_MAX_LENGTH


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z', max_length=MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())])
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "email", "id", "username", "first_name", "last_name",
            "is_subscribed"
        )
        model = User

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            return current_user.subscriber.filter(author=obj).exists()
        return False


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z',
                                      required=True, max_length=MAX_LENGTH)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        read_only_fields = ('id', )

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_username(self, value):
        if (
            value.lower() == 'me'
        ):
            raise serializers.ValidationError(
                'Нельзя указывать me в качестве имени')
        return value


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})
    new_password = serializers.CharField(style={"input_type": "password"})

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


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AuthorSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id", "username", "email", "first_name", "last_name",
            "is_subscribed", "recipes", "recipes_count"
        )

    def get_recipes(self, obj):
        recipes_limit = int(
            self.context['request'].query_params['recipes_limit']
        )
        return RecipeSerializer(
            obj.recipes.all()[:recipes_limit], many=True
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            return current_user.subscriber.filter(author=obj).exists()
        return False
