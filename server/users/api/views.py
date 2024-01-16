from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.db import transaction
from users.models import User
from core.utils import get_object_or_none
import jwt
from django.utils.timezone import now, timedelta
from decouple import config

from .serializers import UserSerializer

class SignupView(APIView):

    @transaction.atomic
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()
        new_user.set_password(request.data['password'])
        new_user.save()

        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email, password = request.data['email'], request.data['password']
        user = get_object_or_none(User, email=email)
        if not user or not user.check_password(password):
            raise AuthenticationFailed('Invalid login')
        payload = {
            'id': user.id,
            'exp': now() + timedelta(days=2),
            'iat': now()
        }
        token = jwt.encode(payload, config('JWT_SECRET'), algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token,httponly=True)
        response.data = {
            'jwt': token
        }

        return response
    

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        try:
            payload = jwt.decode(token, config('JWT_SECRET'), algorithms='HS256')

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")

        user = get_object_or_none(User, id=payload['id'])
        user_data = UserSerializer(user).data
        return Response(user_data)
    

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': "success"
        }

        return response