from django.urls import path, re_path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
    TokenObtainPairView,
)

from django_app import views
from django.views.generic import RedirectView
from django_app.swagger import urlpatterns as doc_urls

urlpatterns = [
    path("", RedirectView.as_view(url="/app/")),
    path("home/", views.home, name="home"),
    path("login_view/", views.login_view, name="login_view"),
    path("logout/", views.logout, name="logout"),
    # ! JWT TOKENS
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/token/verify/", TokenVerifyView.as_view()),
]


urlpatterns += doc_urls

urlpatterns += [
    re_path(r"^app/.*$", views.react_app, name="reac_app"),
]
