from django.urls import path
from ..views.password_views import ChangePasswordView

urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
