"""
Views for user api
"""
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _

from rest_framework import (
    generics,
    authentication,
    permissions,
    viewsets,
    status)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    LogoutSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticted user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class LoginView(generics.GenericAPIView):
    """Authenticate the user, login and generate token"""
    serializer_class = AuthTokenSerializer
    allowed_methods = ['POST']

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogOutView(generics.GenericAPIView):
    """Delete user token on successful logout token in request.data field"""
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = LogoutSerializer
    allowed_methods = ['POST']

    def post(self, request):
        return self.logout(request)

    def logout(self, request):
        # print(request.user)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                Token.objects.filter(user=serializer.validated_data['user']).delete()
                logout(request)
                return Response({"success": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)
            except (AttributeError, ObjectDoesNotExist):
                return Response({"fail": _("Token not found")}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)




