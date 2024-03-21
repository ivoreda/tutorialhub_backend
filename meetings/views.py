from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class CreateMeetingView(APIView):
    def post(self, request):
        pass

class GetAllTutorMeetingsView(APIView):
    def get(self, request):
        pass

class GetAllTuteeMeetingsView(APIView):
    def get(self, request):
        pass

class GetSingleMeetingView(APIView):
    def get(self, request):
        pass

class GetAllMeetingsView(APIView):
    def get(self, request):
        pass
