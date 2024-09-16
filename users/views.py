from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import User
from .serializers import UserSerializer
import jwt, datetime


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User does not exist')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='token', value=token, httponly=True)
        response.data = {'jwt': token}
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzI2NTcxNDYzLCJpYXQiOjE3MjY0ODUwNjN9.0hbrp3ukcAtrjyXN5YiNh22hAFFt0g77PzkTw2lLAPg"


        if not token:
            raise AuthenticationFailed("unauthenticated")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired')

        user = User.objects.get(id=payload['id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)


class logoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            "message": "successfully logged out"
        }
        return response




