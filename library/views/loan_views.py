from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from ..services.loan_service import LoanService
from ..serializers.loan_serializers import LoanSerializer, LoanCreateSerializer
from ..filters import LoanFilter
from ..permissions import IsAdminUser, IsRegisteredUser

class BorrowBookView(APIView):
    permission_classes = [IsRegisteredUser]  # Only registered users can borrow books

    @swagger_auto_schema(
        operation_description="Borrow a book",
        responses={201: LoanSerializer, 400: "Book not available"}
    )
    def post(self, request, book_id):
        serializer = LoanCreateSerializer(data={}, context={'book_id': book_id})
        if serializer.is_valid():
            loan = LoanService.borrow_book(request.user, book_id)
            if loan:
                return Response(LoanSerializer(loan).data, status=status.HTTP_201_CREATED)
            return Response({"detail": "Book not available."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(APIView):
    permission_classes = [IsRegisteredUser]  # Only registered users can return books

    @swagger_auto_schema(
        operation_description="Return a borrowed book",
        responses={200: LoanSerializer, 400: "No active loan found"}
    )
    def post(self, request, book_id):
        loan = LoanService.return_book(request.user, book_id)
        if loan:
            return Response(LoanSerializer(loan).data, status=status.HTTP_200_OK)
        return Response({"detail": "No active loan found for this book."}, status=status.HTTP_400_BAD_REQUEST)    

class LoanListView(APIView):
    permission_classes = [IsAdminUser]  # Only admins can view loaned books
    filter_backends = [DjangoFilterBackend]
    filterset_class = LoanFilter
    pagination_class = PageNumberPagination 


    @swagger_auto_schema(
        operation_description="List all loaned books",
        responses={200: LoanSerializer(many=True)}
    )
    def get(self, request):
        loans = LoanService.get_all_loans()
        filtered_loans = DjangoFilterBackend().filter_queryset(request, loans, self)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(filtered_loans, request)
        serializer = LoanSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)