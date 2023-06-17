from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import SubscriptionListView, follow_author

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register(
    r'users/subscriptions',
    SubscriptionListView,
    basename='subscriptions',
)

urlpatterns = [
    path('users/<int:pk>/subscribe/',
         follow_author,
         name='follow-author'),
    path(r'', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/token/login/',
         TokenCreateView.as_view(),
         name='login'),
    path('auth/token/logout/',
         TokenDestroyView.as_view(),
         name='logout'),
]
