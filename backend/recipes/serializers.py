import traceback

from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import CustomUser

from .models import (FavoriteRecipe, Ingredient, IngredientsRecipe, Recipe,
                     ShoppingCart, Tag)


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id'
    )
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    slug = serializers.SlugField()

    class Meta:
        model = Tag
        fields = '__all__'
        lookup_field = 'slug'


class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientsRecipeSerializer(
        many=True, source='recipe_ingredients'
    )
    image = Base64ImageField(
        max_length=None, use_url=True,
    )
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(max_value=32767, min_value=1)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def get_status_func(self, data):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        try:
            user = self.context.get('request').user
        except:
            user = self.context.get('user')
        callname_function = format(traceback.extract_stack()[-2][2])
        if callname_function == 'get_is_favorited':
            init_queryset = FavoriteRecipe.objects.filter(
                recipe=data.id,
                user=user
            )
        elif callname_function == 'get_is_in_shopping_cart':
            init_queryset = ShoppingCart.objects.filter(recipe=data, user=user)
        if init_queryset.exists():
            return True
        return False

    def get_is_favorited(self, data):
        return self.get_status_func(data)

    def get_is_in_shopping_cart(self, data):
        return self.get_status_func(data)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        ingredient_list = []

        for ingredient in ingredients:
            IngredientsRecipe.ingredient_list.append(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
        IngredientsRecipe.objects.bulk_create(ingredient_list)

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.set(tags)

        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()

            for ingredient in ingredients:
                amount = ingredient['amount']
                ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])

                IngredientsRecipe.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient,
                    defaults={'amount': amount}
                )

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        response = super(RecipeSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class FavoritedSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True, source='recipe.id',
    )
    cooking_time = serializers.CharField(
        read_only=True, source='recipe.cooking_time',
    )
    image = serializers.CharField(
        read_only=True, source='recipe.image',
    )
    name = serializers.CharField(
        read_only=True, source='recipe.name',
    )

    def validate(self, data):
        recipe = data['recipe']
        user = data['user']
        if user == recipe.author:
            raise serializers.ValidationError('You are the author!')
        if (FavoriteRecipe.objects.filter(recipe=recipe, user=user).exists()):
            raise serializers.ValidationError('You have already subscribed!')
        return data

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'cooking_time', 'name', 'image')


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
        source='recipe.id',
    )
    cooking_time = serializers.CharField(
        read_only=True,
        source='recipe.cooking_time',
    )
    image = serializers.CharField(
        read_only=True,
        source='recipe.image',
    )
    name = serializers.CharField(
        read_only=True,
        source='recipe.name',
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'cooking_time', 'name', 'image')
