from ..repositories.loan_repository import LoanRepository
from ..repositories.book_repository import BookRepository
from ..models import Book
from django.utils import timezone

class LoanService:
    @staticmethod
    def get_all_loans():
        return LoanRepository.get_all()

    @staticmethod
    def get_loan_by_id(loan_id):
        return LoanRepository.get_by_id(loan_id)

    @staticmethod
    def create_loan(**kwargs):
        return LoanRepository.create(**kwargs)

    @staticmethod
    def update_loan(loan_id, **kwargs):
        loan = LoanRepository.get_by_id(loan_id)
        if loan:
            return LoanRepository.update(loan, **kwargs)
        return None

    @staticmethod
    def delete_loan(loan_id):
        loan = LoanRepository.get_by_id(loan_id)
        if loan:
            LoanRepository.delete(loan)
            return True
        return False

    @staticmethod
    def borrow_book(user, book_id):
        book = BookRepository.get_by_id(book_id)
        if book.availability:
            loan = LoanRepository.create(user=user, book=book)
            book.availability = False
            book.save()
            return loan
        return None

    @staticmethod
    def return_book(user, book_id):
        loan = LoanRepository.model.objects.filter(user=user, book_id=book_id, returned_date__isnull=True).first()
        if loan:
            loan.returned_date = timezone.now()
            loan.book.availability = True
            loan.book.save()
            loan.save()
            return loan
        return None