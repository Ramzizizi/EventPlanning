"""
URL configuration for event_planning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views

from events import urls as event_urls
from places import urls as place_urls

# подключение рутов из приложений
urlpatterns = [
    path("", include("events.urls")),
    path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("events/", event_urls.event_list),
                path("events/<int:pk>/", event_urls.event_detail),
                path("events/<int:pk>/visitor/", event_urls.visitors_detail),
                path("places/", place_urls.base_places_list),
                path("places/<str:place_type>/", place_urls.places_list),
                path(
                    "places/<str:place_type>/<int:pk>/",
                    place_urls.places_detail,
                ),
                path(
                    "token/",
                    views.TokenObtainPairView.as_view(),
                    name="token_obtain_pair",
                ),
                path(
                    "token/refresh/",
                    views.TokenRefreshView.as_view(),
                    name="token_refresh",
                ),
            ],
        ),
    ),
]
