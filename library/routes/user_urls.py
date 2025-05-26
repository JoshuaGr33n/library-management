from django.urls import path
from ..views.user_views import (
    UserListView, UserDetailView, UserProfileView,
    UserDeactivateView, UserReactivateView
)

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('<int:user_id>/deactivate/', UserDeactivateView.as_view(), name='user-deactivate'),
    path('<int:user_id>/reactivate/', UserReactivateView.as_view(), name='user-reactivate'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
