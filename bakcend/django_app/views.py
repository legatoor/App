from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from django.contrib.auth import authenticate, login, logout


@permission_classes([AllowAny])
def home(request):
    return render(
        request,
        "home.html",
    )


@permission_classes([AllowAny])
def react_app(request):
    return render(request, "index.html")


def logout_view(request):
    logout(request)
    return redirect("login_view")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login.html", context={})
