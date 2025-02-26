from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from ..serializers.password_serializer import ChangePasswordSerializer
from ..services.user_service import UserService

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Change the authenticated user's password",
        request_body=ChangePasswordSerializer,
        responses={
            200: "Password changed successfully",
            400: "Bad Request - Incorrect old password or invalid data",
            401: "Unauthorized - Authentication credentials were not provided"
        }
    )

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                UserService.change_password(
                    user=request.user,
                    old_password=serializer.validated_data['old_password'],
                    new_password=serializer.validated_data['new_password']
                )
                return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)