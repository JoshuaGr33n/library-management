from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Book, Loan
from datetime import timedelta
from django.utils import timezone
from urllib.parse import quote_plus

User = get_user_model()

class BookIntegrationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass", role="admin")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
            availability=True
        )

    def test_anonymous_user_can_view_books(self):
        url = reverse('book-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_book(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('book-list-create')
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "9876543210987",
            "page_count": 300,
            "availability": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_delete_book(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

class LoanFilterIntegrationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass", role="admin")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
            availability=True
        )
        self.loan1 = Loan.objects.create(
            user=self.user,
            book=self.book,
            borrowed_date=timezone.now() - timedelta(days=10)
        )
        self.loan2 = Loan.objects.create(
            user=self.user,
            book=self.book,
            borrowed_date=timezone.now() - timedelta(days=5),
            returned_date=timezone.now() - timedelta(days=2)
        )
        self.loan3 = Loan.objects.create(
            user=self.user,
            book=self.book,
            borrowed_date=timezone.now() - timedelta(days=15),
            returned_date=timezone.now() - timedelta(days=11)
        )
        self.loan4 = Loan.objects.create(
            user=self.user,
            book=self.book,
            borrowed_date=timezone.now() - timedelta(days=3),
        )

    def test_filter_loans_by_borrowed_date(self):
        self.client.force_authenticate(user=self.admin)
        start_datetime = timezone.now() - timedelta(days=7)
        end_datetime = timezone.now()
        start_iso = quote_plus(start_datetime.replace(microsecond=0).isoformat().replace('+00:00','Z'))
        end_iso = quote_plus(end_datetime.replace(microsecond=0).isoformat().replace('+00:00','Z'))
        url = reverse('loan-list') + f'?borrowed_date_after={start_iso}&borrowed_date_before={end_iso}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
        
    def test_filter_active_loans(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('loan-list') + '?is_active=true'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Loan 1 and 4 are active