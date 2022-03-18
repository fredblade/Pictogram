from rest_flex_fields.views import FlexFieldsMixin

from .serializers import RegisterSerializer, ChangePasswordSerializer, UpdateUserSerializer, GetUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework import permissions


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# class GetView(generics.ListAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = GetUserSerializer

class GetUserIdView(FlexFieldsMixin, APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        print("USERID", user_id)
        # postitems = PostItem.objects.filter(user=request.user.id)
        useritem = User.objects.filter(id=user_id).first()
        serializer = GetUserSerializer(useritem)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GetUserSerializer

    def get(self, request):
        print(self.request.user)
        serializer = GetUserSerializer(request.user)
        return Response(serializer.data)


class GetListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = GetUserSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)
