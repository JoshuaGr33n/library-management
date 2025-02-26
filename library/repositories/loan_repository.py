from .base_repository import BaseRepository
from ..models import Loan

class LoanRepository(BaseRepository):
    model = Loan