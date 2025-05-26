from django.urls import path
from ..views.book_views import BookListCreateView, BookDetailView
from ..views.loan_views import BorrowBookView, ReturnBookView

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book-list-create'),
    path('<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('<int:book_id>/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('<int:book_id>/return/', ReturnBookView.as_view(), name='return-book'),
]
