from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Book, Loan
from ..serializers.user_serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    UserProfileSerializer
)
from ..serializers.book_serializers import BookSerializer
from ..serializers.loan_serializers import LoanSerializer, LoanCreateSerializer

User = get_user_model()

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
        "id": 6,
        "username": "testuser",
        "email": "testuser@example.com",
        "phone_number": "1234567890",
        "role": "user",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data, self.user_data)

    def test_user_serializer_validation(self):
        invalid_data = {
            "username": "",  # Username is required
            "email": "invalid-email",  # Invalid email format
            "phone_number": "1234567890",
            "role": "user"
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
        self.assertIn("email", serializer.errors)

class UserRegistrationSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123",
            "phone_number": "1234567890",
            "role": "user"
        }

    def test_user_registration_serializer(self):
        serializer = UserRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, self.valid_data["username"])
        self.assertEqual(user.email, self.valid_data["email"])

    def test_user_registration_serializer_validation(self):
        invalid_data = {
            "username": "",  # Username is required
            "email": "invalid-email",  # Invalid email format
            "password": "short",  # Password too short
            "phone_number": "1234567890",
            "role": "user"
        }
        serializer = UserRegistrationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)

class UserUpdateSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            phone_number="1234567890",
            role="user"
        )
        self.valid_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "phone_number": "0987654321",
            "role": "admin"
        }

    def test_user_update_serializer(self):
        serializer = UserUpdateSerializer(instance=self.user, data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, self.valid_data["username"])
        self.assertEqual(updated_user.email, self.valid_data["email"])

class UserProfileSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            phone_number="1234567890",
            role="user"
        )
        self.user_data = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "phone_number": self.user.phone_number,
            "role": self.user.role,
            "is_active": self.user.is_active
        }

    def test_user_profile_serializer(self):
        serializer = UserProfileSerializer(instance=self.user)
        self.assertEqual(serializer.data, self.user_data)

    def test_user_profile_serializer_update(self):
        data = {
            "username": "updatedprofile",
            "email": "updatedprofile@example.com",
            "phone_number": "1122334455"
        }
        serializer = UserProfileSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, data["username"])
        self.assertEqual(updated_user.email, data["email"])

class BookSerializerTest(TestCase):
    def setUp(self):
        self.book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "1234567890123",
            "page_count": 200,
            "availability": True
        }
        self.book = Book.objects.create(**self.book_data)
        self.book_data['id'] = self.book.id

    def test_book_serializer(self):
        serializer = BookSerializer(instance=self.book)
        self.assertEqual(serializer.data, self.book_data)

    def test_book_serializer_validation(self):
        invalid_data = {
            "title": "",  # Title is required
            "author": "Test Author",
            "isbn": "1234567890123",
            "page_count": 200,
            "availability": True
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

class LoanSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
            availability=True
        )
        self.loan = Loan.objects.create(user=self.user, book=self.book)

    def test_loan_serializer(self):
        serializer = LoanSerializer(instance=self.loan)
        self.assertEqual(serializer.data["user"]["id"], self.user.id)
        self.assertEqual(serializer.data["book"]["id"], self.book.id)

class LoanCreateSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
            availability=True
        )

    def test_loan_create_serializer_validation(self):
        # Test valid data
        serializer = LoanCreateSerializer(data={}, context={"book_id": self.book.id})
        self.assertTrue(serializer.is_valid())

        # Test invalid book ID
        serializer = LoanCreateSerializer(data={}, context={"book_id": 999})
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

        # Test unavailable book
        self.book.availability = False
        self.book.save()
        serializer = LoanCreateSerializer(data={}, context={"book_id": self.book.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)