from rest_framework import generics, status, views, permissions, viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth import authenticate, login, logout
from .serializers import (
    SignUpSerializer, ProfileSerializer, LoginSerializer, UpdatePasswordSerializer
)
from .tokens import create_jwt_pair_for_user
# Create your views here.


class SignUpView(generics.GenericAPIView):
    """View for handling user signup."""
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request):
        """Validating a POST request to create a new user."""
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "User is created successfully!",
                "info": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    """View for handling user login."""
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: Request):
        """Validating the POST request for user login."""
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            tokens = create_jwt_pair_for_user(user)
            content = {
                "message": "Login Successfully",
                "tokens": tokens
            }
            login(request, user)
            return Response(data=content, status=status.HTTP_200_OK)
        return Response(data={"message": "Invalid username or password!!!"})

    def get(self, request: Request):
        """Handle GET request to retrieve current user and auth data."""
        content = {
            "user": str(request.user),
            "auth": str(request.auth),
        }

        return Response(data=content, status=status.HTTP_200_OK)


class LogoutView(views.APIView):
    """View for handling user logout."""
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        logout(request)
        return Response('You logged out!!!', status=status.HTTP_200_OK)


class UpdatePasswordViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """ViewSet for handling password change operations."""
    serializer_class = UpdatePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the current user as the object."""
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        old_password = request.data.get('old_password')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        user = self.request.user

        if not user.check_password(old_password):
            raise ValidationError("Invalid Old Password!!!")
        if password != password2:
            raise ValidationError("Passwords do not match!!!")

        user.set_password(password)
        user.save()

        return Response(data={"message": "Password updated!!!"}, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for handling user profile operations."""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the current user as the object."""
        print(self.request.user.nickname)
        return self.request.user
