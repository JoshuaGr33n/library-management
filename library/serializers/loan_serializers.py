from rest_framework import serializers
from ..models import Loan, Book
from .user_serializers import UserSerializer
from .book_serializers import BookSerializer

class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'user', 'book', 'borrowed_date', 'returned_date']

class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = []  

    def validate(self, data):
        book_id = self.context['book_id']
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")

        if not book.availability:
            raise serializers.ValidationError("This book is not available for borrowing.")

        return data