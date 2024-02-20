from django.urls import path

from users.views import UserViews


urlpatterns = [
    path("login/", UserViews.req_login, name="login"),
    path("logout/", UserViews.req_logout, name="logout"),
]
