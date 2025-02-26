from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..services.user_service import UserService
from ..serializers.user_serializers import (
    UserSerializer, UserUpdateSerializer, UserProfileSerializer
)
from ..permissions import IsAdminUser, IsRegisteredUser

class UserListView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Retrieve a list of all users (Admin only)",
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request):
        users = UserService.get_all_users()
        serializer = UserSerializer(users, many=True)
        return Response({
            'message': 'Users retrieved successfully',
            'data': serializer.data
        })

class UserDetailView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific user by ID (Admin only)",
        responses={200: UserSerializer(), 404: "User not found"}
    )
    def get(self, request, user_id):
        user = UserService.get_user_by_id(user_id)
        if user:
            serializer = UserSerializer(user)
            return Response({
                'message': 'User retrieved successfully',
                'data': serializer.data
            })
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update user details (Admin only)",
        request_body=UserUpdateSerializer,
        responses={200: UserUpdateSerializer(), 400: "Bad Request", 404: "User not found"}
    )
    def put(self, request, user_id):
        user = UserService.get_user_by_id(user_id)
        if user:
            serializer = UserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'User updated successfully',
                    'data': serializer.data
                })
            return Response({'message': 'Bad request', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete a user by ID (Admin only)",
        responses={204: "User deleted successfully", 404: "User not found"}
    )
    def delete(self, request, user_id):
        if UserService.delete_user(user_id):
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    permission_classes = [IsRegisteredUser]

    @swagger_auto_schema(
        operation_description="Retrieve the authenticated user's profile",
        responses={200: UserProfileSerializer()}
    )
    def get(self, request):
        user = UserService.get_user_profile(request.user)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update the authenticated user's profile",
        request_body=UserProfileSerializer,
        responses={
            200: UserProfileSerializer(),
            400: "Bad Request",
            404: "User not found"
        }
    )
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = UserService.update_user(request.user.id, **serializer.validated_data)
            if updated_user:
                return Response(UserProfileSerializer(updated_user).data)
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeactivateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Deactivate a user (Admin only)",
        responses={
            200: "User deactivated successfully",
            404: "User not found"
        }
    )
    def post(self, request, user_id):
        if UserService.deactivate_user(user_id):
            return Response({"detail": "User deactivated successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class UserReactivateView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Reactivate a user (Admin only)",
        responses={
            200: "User reactivated successfully",
            404: "User not found"
        }
    )
    def post(self, request, user_id):
        if UserService.reactivate_user(user_id):
            return Response({"detail": "User reactivated successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)