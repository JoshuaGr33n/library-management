from .base_repository import BaseRepository
from ..models import Book

class BookRepository(BaseRepository):
    model = Book