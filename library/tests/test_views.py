from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Book, Loan

User = get_user_model()

class UserAPITest(APITestCase):
    def setUp(self):
        # Create a regular user and an admin user
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin = User.objects.create_user(username="admin", password="adminpass", role="admin")
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        url = reverse('register')
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123",
            "phone_number": "1234567890",
            "role": "user"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_get_user_list_admin(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

    def test_get_user_detail_admin(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['username'], self.user.username)

    def test_update_user_detail_admin(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', args=[self.user.id])
        data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "phone_number": "0987654321",
            "role": "user"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['username'], "updateduser")

    def test_delete_user_admin(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_get_user_profile(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_user_profile(self):
        url = reverse('user-profile')
        data = {
            "username": "updatedprofile",
            "email": "updatedprofile@example.com",
            "phone_number": "1122334455"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "updatedprofile")

    def test_deactivate_user_admin(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        url = reverse('user-deactivate', args=[self.user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_reactivate_user_admin(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        self.user.is_active = False
        self.user.save()
        url = reverse('user-reactivate', args=[self.user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

class BookAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin = User.objects.create_user(username="admin", password="adminpass", role="admin")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
            availability=True
        )
        self.client.force_authenticate(user=self.user)

    def test_get_books(self):
        url = reverse('book-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_create_book_admin(self):
        # Authenticate as admin
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

    def test_get_book_detail(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book_admin(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        url = reverse('book-detail', args=[self.book.id])
        data = {
            "title": "Test Book",
            "author": "Updated Author",
            "isbn": "1234567890123",
            "page_count": 250,
            "availability": False
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Book")

    def test_delete_book_admin(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

class LoanAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin = User.objects.create_user(username="admin", password="adminpass", role="admin")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
            availability=True
        )
        self.client.force_authenticate(user=self.user)

    def test_borrow_book(self):
        url = reverse('borrow-book', args=[self.book.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Loan.objects.filter(user=self.user, book=self.book).exists())

    def test_return_book(self):
        Loan.objects.create(user=self.user, book=self.book)
        url = reverse('return-book', args=[self.book.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Loan.objects.filter(user=self.user, book=self.book, returned_date__isnull=False).exists())

    def test_get_loans_admin(self):
        # Authenticate as admin
        self.client.force_authenticate(user=self.admin)
        Loan.objects.create(user=self.user, book=self.book)
        url = reverse('loan-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)