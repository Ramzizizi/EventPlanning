from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic import View


class UserViews(View):

    @staticmethod
    def req_login(request):
        user = authenticate(
            request,
            username=request.POST["email"],
            password=request.POST["pass"],
        )
        if user is not None:
            login(request, user)
        return redirect("/")

    @staticmethod
    def req_logout(request):
        user = request.user
        if user.is_authenticated:
            logout(request)
        return redirect("/")
