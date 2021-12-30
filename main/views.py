import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import SportGame
from main.serializers import UserSerializer, GameSerializer


@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def sign_up(request):
    try:
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        if password1 == password2:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                data = {
                    "success": False,
                    "message": "Bunday foydalanuvchi mavjud"
                }
                return Response(data, status=405)
            else:
                us = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=make_password(password1))
                us.save()
                data = {
                    "success": True,
                    "message": "Welcome!!!"
                }
        else:
            data = {
                "success": False,
                "message": "Parollar to'g'ri kelmadi!!!"
            }
            return Response(data, status=405)
    except Exception as e:
        data = {
            "success": False,
            "message": f"{e}"
        }
        return Response(data, status=405)
    return Response(data, status=200)


@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        us = User.objects.get(username=username)
        if check_password(password, us.password):
            user = UserSerializer(us)
            token = RefreshToken.for_user(us)
            tk = {
                "refresh": str(token),
                "access": str(token.access_token)
            }
            data = {
                "success": True,
                "message": "Kirish tasdiqlandi",
                "data": {
                    "user": user.data,
                    "token": tk
                }
            }
        else:
            data = {
                "success": False,
                "message": "Username yoki parol xato!!!"
            }
            return Response(data, status=405)
    except Exception as e:
        data = {
            "success": False,
            "message": f"{e}"
        }
        return Response(data, status=405)
    return Response(data, status=200)


@api_view(['get'])
@authentication_classes([])
@permission_classes([])
def get_games(request):
    try:
        minimal = datetime.datetime.now()
        maximal = datetime.datetime.now() + datetime.timedelta(hours=720)
        games = SportGame.objects.filter(Q(date__gte=minimal) and Q(date__lte=maximal))
        games_data = GameSerializer(games, many=True)
        data = {
            "success": True,
            "data": games_data.data
        }
    except Exception as e:
        data = {
            "success": False,
            "message": "{}".format(e)
        }
        return Response(data, status=405)
    return Response(data, status=200)
