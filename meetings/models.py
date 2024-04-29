from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.

class Meeting(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_meetings')
    tutee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutee_meetings')
    description = models.TextField()
    meeting_link = models.CharField(max_length=100)
    feedback = models.TextField()
    meeting_date = models.DateField()
    meeting_start_time = models.TimeField()
    meeting_end_time = models.TimeField()


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tutor.first_name + " " + self.tutor.last_name + " meeting with " + self.tutee.first_name + " " + self.tutee.last_name
