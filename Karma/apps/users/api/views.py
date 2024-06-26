from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken, 
    BlacklistedToken
)

from .serializers import (
    UserListSerializer,
    UserUpdateDestroySerializer,
    UserLoginSerializer,
    RegisterSerializer,
    PasswordResetSerializer
)

User = get_user_model()


class UserListAPIView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated,)


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserUpdateDestroySerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated, )


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.filter(is_active=True)

    def post(self,request): 
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        if email and password:
            user_obj = User.objects.filter(email__iexact=email).first()
            if user_obj and user_obj.check_password(password):
                user = UserLoginSerializer(user_obj)
                data_list = {}
                data_list.update(user.data)
                return Response({"message": "Login Successfully", "data":data_list, "code": 200})
            else:
                message = "Unable to login with given credentials"
                return Response({"message": message , "code": 500, 'data': {}} )
        else:
            message = "Invalid login details."
            return Response({"message": message , "code": 500, 'data': {}})
        

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT,)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllDevicesAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_205_RESET_CONTENT)
    

class PasswordResetAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            form = PasswordResetForm(data={'email': email})
            user_obj = User.objects.filter(email__iexact=email).first()

            if form.is_valid():
                if user_obj:
                    form.save(request=request)
                    return Response({'detail': 'Password reset email has been sent.'})
                else :
                    return Response({'detail': 'You have not registered yet'})
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)