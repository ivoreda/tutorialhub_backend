from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
import random

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
            ("Tutor", "Tutor"),
            ("Tutee", "Tutee"),
            ("Admin", "Admin"),)

    GENDER = (("Male", "Male"),
        ("Female", "Female"))
    # student_performance = models.IntegerField(blank=True, null=True)  # Assuming not all users will have this field set
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER, default="Male")
    profile_picture = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # 'email' is already the username field

    def __str__(self):
        return self.email


class Tutor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    meetings_created = models.IntegerField(default=0)
    hours_spent = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Tutee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    tutee_performance = models.IntegerField(default=0)
    meetings_attended = models.IntegerField(default=0)
    hours_spent = models.IntegerField(default=0)
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, related_name='tutees', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "Tutor":
            Tutor.objects.create(user=instance)
        elif instance.user_type == "Tutee":
            tutee = Tutee.objects.create(user=instance)
            tutors = list(Tutor.objects.all())
            if tutors:
                random_tutor = random.choice(tutors)
                tutee.tutor = random_tutor
                tutee.save()

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'tutor'):
        instance.tutor.save()
    if hasattr(instance, 'tutee'):
        instance.tutee.save()
