from django import views
from django.urls import path
from .views import profile, profile_details, promote_to_leader, register, certificate_list, skill_list, delete_certificate, delete_skill
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', register),
    path('login/', TokenObtainPairView.as_view()),
    path('profile/', profile),
    path('promote/', promote_to_leader),
    path('profile/details/', profile_details),
    path('certificates/', certificate_list),
    path('certificates/<int:pk>/', delete_certificate),
    path('skills/', skill_list),
    path('skills/<int:pk>/', delete_skill),
]