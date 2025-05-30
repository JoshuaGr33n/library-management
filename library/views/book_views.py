from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from ..services.book_service import BookService
from ..serializers.book_serializers import BookSerializer
from ..filters import BookFilter
from ..permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from ..utils.swagger_decorators import hide_from_docs_yasg

class BookListCreateView(APIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    pagination_class = PageNumberPagination
    ordering = ['id'] 
    
    # @swagger_auto_schema(
    #     operation_description="List all books",
    #     responses={200: BookSerializer(many=True)}
    # )
    @hide_from_docs_yasg(
        dev_description="List all books",
        dev_response={200: BookSerializer(many=True)}
    )
    def get(self, request):
        books = BookService.get_all_books()
        filtered_books = DjangoFilterBackend().filter_queryset(request, books, self)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(filtered_books, request)
        serializer = BookSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new book",
        request_body=BookSerializer,
        responses={
            201: BookSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request):
        self.permission_classes = [IsAdminUser]  # Only admins can create books
        self.check_permissions(request)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            BookService.create_book(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Retrieve a book by ID",
        responses={200: BookSerializer, 404: "Not Found"}
    )
    def get(self, request, book_id):
        book = BookService.get_book_by_id(book_id)
        if book:
            serializer = BookSerializer(book)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update a book",
        request_body=BookSerializer,
        responses={200: BookSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, book_id):
        self.permission_classes = [IsAdminUser]  # Only admins can update books
        self.check_permissions(request)
        
        book = BookService.get_book_by_id(book_id)
        if book:
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                BookService.update_book(book_id, **serializer.validated_data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a book",
        responses={204: "No Content", 404: "Not Found"}
    )
    def delete(self, request, book_id):
        self.permission_classes = [IsAdminUser]  # Only admins can delete books
        self.check_permissions(request)
        
        if BookService.delete_book(book_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)