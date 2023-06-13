from django.db.models import F, Sum

from .models import ShoppingCart


def get_shopping_list(request):
    ingredients = ShoppingCart.objects.filter(
        user=request.user).values(
        name=F('ingredient__name'),
        measurement_unit=F('ingredient__measurement_unit')
    ).annotate(count=Sum('amount')).values_list(
        'ingredient__name', 'count', 'ingredient__measurement_unit'
    )
    return ingredients
