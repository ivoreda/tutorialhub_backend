from django.urls import path

from . import views

urlpatterns = [
    path('create-meeting/', views.CreateMeetingView.as_view()),
    path('get-all-meetings/', views.GetAllMeetingsView.as_view()),
    path('get-single-meeting/<int:id>', views.GetSingleMeetingView.as_view()),
    path('get-tutor-meetings/', views.GetAllTutorMeetingsView.as_view()),
    path('get-tutee-meetings/', views.GetAllTuteeMeetingsView.as_view()),

]
