from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
)

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(
        url='/static/img/favicon.ico', permanent=True
    )),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('recipes.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(
        url_name='schema'), name='redoc'
    ),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'
    ),
]
