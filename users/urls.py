from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('get-user/', views.GetUserView.as_view()),
    path('get-tutors-tutees/', views.GetTutorsTuteesView.as_view()),
    path('get-all-tutees/', views.AdminGetAllTuteesView.as_view()),
    path('get-all-tutors/', views.AdminGetAllTutorsView.as_view()),
    path('admin-dashboard/', views.AdminDashboardView.as_view()),
    path('user-dashboard/', views.UserDashboardView.as_view()),





    # Add other URLs for your app here
]
