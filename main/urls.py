from django.urls import path

from main.views import sign_up, login, get_games

urlpatterns = [
    path('sign-up', sign_up),
    path('login', login),
    path('get-games', get_games)
]
