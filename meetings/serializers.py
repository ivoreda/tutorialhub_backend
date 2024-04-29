from rest_framework import serializers
from . import models

class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Meeting
        fields = '__all__'

class CreateMeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Meeting
        fields = ["tutee", "description", "meeting_date", "meeting_link",
                    "meeting_start_time", "meeting_end_time",]
