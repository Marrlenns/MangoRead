from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)


PUT = {"put": "update"}
RETRIEVE_UPDATE = {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('update_password/', views.UpdatePasswordViewSet.as_view(PUT)),
    path('profile/', views.ProfileViewSet.as_view(RETRIEVE_UPDATE)),

    path("jwt/create/", TokenObtainPairView.as_view()),
    path("jwt/refresh/", TokenRefreshView.as_view()),
    path("jwt/verify/", TokenVerifyView.as_view()),
]