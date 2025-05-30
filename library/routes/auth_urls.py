from django.urls import path
from ..views.auth_views import UserRegistrationView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
]
