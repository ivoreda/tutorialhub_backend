from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic
from rest_framework.views import APIView
from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from meetings import permissions
from meetings import models as meeting_models


User = get_user_model()


class SignUpView(APIView):
    serializer_class = serializers.SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email').lower()
        full_name = serializer.validated_data.get('first_name') + " " + serializer.validated_data.get('last_name')
        user = serializer.save()
        user_type = serializer.validated_data.get('user_type')
        user.user_type = user_type
        if user_type == "Admin":
            user.is_staff = True
            user.is_active = True
            user.is_superuser = True
        user.username = email.split('@')[0]
        user.save()
        return Response({'status': 'True', 'message': 'user created successfully.', 'data': serializer.data}, status=status.HTTP_201_CREATED)



class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        user_email = self.request.data.get('email').lower()
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({'error': 'User not active. Contact admin to activate your account.'}, status=status.HTTP_400_BAD_REQUEST)
        self.request.data['email'] = user_email
        return super().post(request, *args, **kwargs)


class GetUserView(APIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = self.serializer_class(request.user)
        return Response({"status": True, "message": "user retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)

class GetTutorsTuteesView(APIView):
    serializer_class = serializers.TuteeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tutor = models.Tutor.objects.get(user=request.user)
        except models.Tutor.DoesNotExist:
            return Response({"status": False, "message": "Tutor not found"}, status=status.HTTP_404_NOT_FOUND)
        tutees = models.Tutee.objects.filter(tutor=tutor)
        tutee_serializer = self.serializer_class(tutees, many=True)  # Make sure your serializer can handle multiple objects
        return Response({"status": True, "message": "Data retrieved successfully", "data": tutee_serializer.data}, status=status.HTTP_200_OK)

class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        user_type = user.user_type

        if user_type == "Tutor":
            tutor_id = user.id
            tutees = models.Tutee.objects.filter(tutor=tutor_id).count()
            meetings = user.tutor.meetings_created

            data = {"tutees": tutees, "meetings": meetings}

            return Response({"status": True, "message": "Data retrieved successfully", "data": data}, status=status.HTTP_200_OK)
        elif user_type == "Tutee":
            tutee_id = user.id
            hours_spent = user.tutee.hours_spent
            meetings = user.tutee.meetings_attended

            data = {"hours_spent": hours_spent, "meetings": meetings}

            return Response({"status": True, "message": "Data retrieved successfully", "data": data}, status=status.HTTP_200_OK)

        return Response({"status": False, "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)



"""
Admin Endpoints
"""
class AdminGetAllTuteesView(APIView):
    serializer_class = serializers.TuteeSerializer
    permission_classes = [permissions.IsAdmin]

    def get(self, request):
        tutees = models.Tutee.objects.all()
        tutee_serializer = self.serializer_class(tutees, many=True)  # Make sure your serializer can handle multiple objects
        return Response({"status": True, "message": "Data retrieved successfully", "data": tutee_serializer.data})

class AdminGetAllTutorsView(APIView):
    serializer_class = serializers.TutorSerializer
    permission_classes = [permissions.IsAdmin]

    def get(self, request):
        tutees = models.Tutor.objects.all()
        tutor_serializer = self.serializer_class(tutees, many=True)  # Make sure your serializer can handle multiple objects
        return Response({"status": True, "message": "Data retrieved successfully", "data": tutor_serializer.data})

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        tutees = models.Tutee.objects.all().count()
        tutors = models.Tutor.objects.all().count()
        meetings = meeting_models.Meeting.objects.all().count()

        data = {"tutors": tutors, "tutees": tutees, "meetings": meetings}
        return Response({"status": True, "message": "Data retrieved successfully", "data": data})


"""
End of Admin Endpoints
"""
