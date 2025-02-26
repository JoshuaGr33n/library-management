from django.urls import path
from .views.auth_views import UserRegistrationView, CustomTokenObtainPairView
from .views.user_views import (
    UserListView, UserDetailView, UserProfileView, UserDeactivateView, UserReactivateView
)
from .views.book_views import BookListCreateView, BookDetailView
from .views.loan_views import BorrowBookView, ReturnBookView, LoanListView
from .views.password_views import ChangePasswordView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>', UserDetailView.as_view(), name='user-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:user_id>/deactivate/', UserDeactivateView.as_view(), name='user-deactivate'),
    path('users/<int:user_id>/reactivate/', UserReactivateView.as_view(), name='user-reactivate'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/<int:book_id>/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('books/<int:book_id>/return/', ReturnBookView.as_view(), name='return-book'),
    path('loans/', LoanListView.as_view(), name='loan-list'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]