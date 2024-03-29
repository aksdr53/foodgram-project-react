from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from users.serializers import UserSerializer
from .models import Ingredient, IngredientsAmount, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'amount')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError({
                'amount': 'Количество должно быть больше 0'
            })
        return value


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeListSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            return current_user.users_favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            return current_user.users_shopping_cart.filter(recipe=obj).exists()

    def get_ingredients(self, obj):
        ingredients_amount = IngredientsAmount.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients_amount, many=True).data


class IngredientAmountCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'amount')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Количество должно быть больше 0'
            )
        return value


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountCreateSerializer(many=True)
    image = Base64ImageField(required=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    author = UserSerializer(read_only=True)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'author',
                  'image', 'name', 'text', 'cooking_time')
        read_only_fields = ('author', 'id')

    def validate_ingredients(self, value):
        init_ingredient = self.initial_data['ingredients']
        if not init_ingredient:
            raise serializers.ValidationError(
                'Выберите ингрединет'
            )
        val_ingredients = []
        ingredients = []
        for ingredient in init_ingredient:
            if ingredient['id'] in ingredients:
                raise serializers.ValidationError(
                    'Одинаковые ингредиенты'
                )
            val_ingredients.append(ingredient)
            ingredients.append(ingredient['id'])
        return val_ingredients

    def validate_tags(self, value):
        init_tags = value
        if not init_tags:
            raise serializers.ValidationError(
                'Выберите тег!'
            )
        tags = []
        for tag in init_tags:
            if tag in tags:
                raise serializers.ValidationError(
                    'Одинаковые теги'
                )
            tags.append(tag)
        return tags

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Время должно быть больше 0'
            )
        return value

    def validate_name(self, value):
        for symbol in value:
            if symbol.isalpha():
                return value
        raise serializers.ValidationError(
            'Название не может состоять только из цифр и знаков'
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientsAmount.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount']
            )
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")

        instance.tags.set(tags)

        IngredientsAmount.objects.filter(recipe=instance).delete()

        for ingredient in ingredients:
            amount = ingredient.get('amount')
            IngredientsAmount.objects.create(
                recipe=instance,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=amount
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context={
            'request': self.context.get('request')}).data


class Shopping_cartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
