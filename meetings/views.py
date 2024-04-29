from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.mixins import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import models, serializers, permissions
from users import models as UsersModels
from django.core.mail import EmailMessage
import random
from django.conf import settings
from django.template.loader import render_to_string

User = get_user_model()


# Create your views here.
class CreateMeetingView(APIView):
    serializer_class = serializers.CreateMeetingSerializer
    permission_classes = [IsAuthenticated, permissions.IsTutor]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            tutee_email = (serializer.validated_data.get("tutee"))

            tutee = User.objects.filter(email=tutee_email).first()

            tutee_full_name = tutee.first_name + " " + tutee.last_name
            tutor_full_name = request.user.first_name + " " + request.user.last_name

            meeting_details = serializer.save(tutor=request.user)

            send_tutor_email(tutor_email=request.user.email,tutee=tutee_full_name ,meeting_details=meeting_details)
            send_tutee_email(tutee_email=tutee_email, tutor=tutor_full_name, meeting_details=meeting_details )

            return Response({"status": True, "message":"Meeting created successfully"}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


def send_tutor_email(tutor_email, tutee, meeting_details):
    subject = f"Meeting with tutee {tutee}."
    from_email = settings.EMAIL_HOST_USER
    email_template = render_to_string(
        'registration/tutor_meeting_email.html', {'email': tutor_email, 'meeting_start_time': meeting_details.meeting_start_time,
                                                    'meeting_end_time': meeting_details.meeting_end_time,
                                                    'meeting_link': meeting_details.meeting_link,
                                                    'meeting_date': meeting_details.meeting_date,
                                                    'tutee':tutee})
    email_verification_email = EmailMessage(
        subject, email_template, from_email, [tutor_email]
    )
    email_verification_email.fail_silently = True
    email_verification_email.send()

def send_tutee_email(tutee_email, tutor, meeting_details):
    subject = f"Meeting with tutee {tutor}."
    from_email = settings.EMAIL_HOST_USER
    email_template = render_to_string(
        'registration/tutor_meeting_email.html', {'email': tutee_email, 'meeting_start_time': meeting_details.meeting_start_time,
                                                    'meeting_end_time': meeting_details.meeting_end_time,
                                                    'meeting_link': meeting_details.meeting_link,
                                                    'meeting_date': meeting_details.meeting_date,
                                                    'tutor':tutor})
    email_verification_email = EmailMessage(
        subject, email_template, from_email, [tutee_email]
    )
    email_verification_email.fail_silently = True
    email_verification_email.send()


class GetAllTutorMeetingsView(APIView):
    serializer_class = serializers.MeetingSerializer
    permission_classes = [permissions.IsTutor]

    def get(self, request):
        try:
            tutor_meetings = models.Meeting.objects.filter(tutor=request.user)
            serializer = self.serializer_class(all_meetings, many=True)
            return Response({"status": True, "message":"Data retrieved successfully", "data":serializer.data}, status=status.HTTP_200_OK)
        except models.Meeting.DoesNotExist:
            return Response({"status": False, "message": "Meetings not found"}, status=status.HTTP_404_NOT_FOUND)


class GetAllTuteeMeetingsView(APIView):
    serializer_class = serializers.MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tutee_meetings = models.Meeting.objects.filter(tutee=request.user)
            serializer = self.serializer_class(all_meetings, many=True)
            return Response({"status": True, "message":"Data retrieved successfully", "data":serializer.data}, status=status.HTTP_200_OK)
        except models.Meeting.DoesNotExist:
            return Response({"status": False, "message": "Meetings not found"}, status=status.HTTP_404_NOT_FOUND)



class GetSingleMeetingView(APIView):
    serializer_class = serializers.MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        meeting_id = kwargs.get('id')  # Retrieve the id from the URL
        try:
            meeting = models.Meeting.objects.get(id=meeting_id)  # Attempt to get the specific meeting by id
            serializer = self.serializer_class(meeting)
            return Response({"status": True, "message": "Meeting retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        except models.Meeting.DoesNotExist:
            return Response({"status": False, "message": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND)


class GetAllMeetingsView(APIView):
    serializer_class = serializers.MeetingSerializer
    permission_classes = [permissions.IsAdmin]

    def get(self, request):
        try:
            all_meetings = models.Meeting.objects.all()
            serializer = self.serializer_class(all_meetings, many=True)
            return Response({"status": True, "message":"Data retrieved successfully", "data":serializer.data}, status=status.HTTP_200_OK)
        except models.Meeting.DoesNotExist:
            return Response({"status": False, "message": "Meetings not found"}, status=status.HTTP_404_NOT_FOUND)
