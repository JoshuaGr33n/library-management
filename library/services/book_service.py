from ..repositories.book_repository import BookRepository

class BookService:
    @staticmethod
    def get_all_books():
        return BookRepository.get_all()

    @staticmethod
    def get_book_by_id(book_id):
        return BookRepository.get_by_id(book_id)

    @staticmethod
    def create_book(**kwargs):
        return BookRepository.create(**kwargs)

    @staticmethod
    def update_book(book_id, **kwargs):
        book = BookRepository.get_by_id(book_id)
        if book:
            return BookRepository.update(book, **kwargs)
        return None

    @staticmethod
    def delete_book(book_id):
        book = BookRepository.get_by_id(book_id)
        if book:
            BookRepository.delete(book)
            return True
        return False