from datetime import datetime
import jwt
import redis
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.urls import reverse
from rest_framework import generics, permissions, status
from rest_framework import views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.payments.models import Subscription
from apps.users.api.serializers import RegisterSerializer, EmailVerificationSerializer, MyTokenObtainPairSerializer, \
    UpdatePasswordSerializer
from apps.users.models import User
from apps.users.tasks import activate_user

# Redis Client
redis_client = redis.Redis(host=f"localhost", port=6379, db=1, decode_responses=True)


# LOGIN
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# REGISTRATION
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        # our access token
        token = RefreshToken.for_user(user).access_token
        # our current domain
        current_site = get_current_site(request).domain
        # email verify link
        relative_link = reverse('email-verify')
        # absolute path
        abs_url = f'http://{current_site}{relative_link}?token={token}'
        # email body
        email_body = f'Hi {user.username}, use link below to verify\n{abs_url}'
        data = {'email_body': email_body, 'email_subject': 'Verify your email', 'receivers': user.email}
        activate_user.delay(data)
        return Response(user_data, status.HTTP_201_CREATED)


# VERIFICATION
class VerifyEmailAPIView(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'success activate'}, status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as ex:
            return Response({'error': 'activation is expired'}, status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError as ex:
            return Response({'error': 'invalid token'}, status.HTTP_400_BAD_REQUEST)


# UPDATE PASSWORD
class UpdatePasswordAPIView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        # return new token
        return Response('success', status=status.HTTP_200_OK)


# LOGOUT
class LogoutAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response('successful logout', status=status.HTTP_205_RESET_CONTENT)
        except Exception as ex:
            return Response(f'{ex}', status=status.HTTP_400_BAD_REQUEST)


class VerifyJWT(views.APIView):
    def get(self, request: Request):
        try:
            token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if user is not None:
                return Response({"message": "JWT is valid"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "JWT is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        except (IndexError, jwt.DecodeError):
            return Response({"message": "JWT is invalid"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def verify_jwt(request: Request):
    try:
        token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        access_token = AccessToken(token=token)
        access_token.check_exp()
        return Response("JWT is valid", status=status.HTTP_200_OK)
    except (IndexError, jwt.DecodeError):
        return Response({"message": "JWT is invalid"}, status=status.HTTP_401_UNAUTHORIZED)
    except (jwt.exceptions.ExpiredSignatureError, KeyError):
        return Response({"message": "JWT is expired"}, status=status.HTTP_401_UNAUTHORIZED)


# RESET PASSWORD REQUEST TODO
class ResetPasswordRequestAPIView(views.APIView):
    def get(self, request):
        pass


# SET NEW PASSWORD TODO
class SetNewPasswordAPIView(views.APIView):
    def post(self):
        pass


# DELETE USER TODO
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request: Request):
    pass


# TODO

@api_view(['GET'])
def lol(request: Request):
    today = datetime.today()
    # s1 = Subscription.objects.all().filter(type=1).first()
    # dt2 = s1.expire_date
    # Active subscriptions
    subscriptions = Subscription.objects.all().filter(Q(expire_date__lt=today) & Q(type=1))
    # today = datetime.today().date()
    # subscriptions = Subscription.objects.all().filter(type=1)
    for subscription in subscriptions:
        subscription.type = 2
        subscription.save()
        # expire_date = subscription.expire_date.date()
        # if expire_date > today:
        #     subscription.type = 2
        #     subscription.save()
    return Response('', status=status.HTTP_200_OK)
