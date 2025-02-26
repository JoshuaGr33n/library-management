from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Book, Loan

User = get_user_model()

class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            page_count=200,
            availability=True
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertTrue(self.book.availability)

class LoanModelTest(TestCase):
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

    def test_loan_creation(self):
        self.assertEqual(self.loan.user.username, "testuser")
        self.assertEqual(self.loan.book.title, "Test Book")
        self.assertIsNone(self.loan.returned_date)