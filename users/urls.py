from django import views
from django.urls import path
from .views import PromoteToLeaderView, SearchUserByUniversityIdView, StaffChangePasswordView, StudentPostListView, add_member, get_club_members, profile, profile_details, promote_to_leader, public_profile_details, register, certificate_list, search_user, skill_list, delete_certificate, delete_skill, user_certificates, user_posts, user_skills
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

urlpatterns = [
    path('register/', register),
    path('login/', TokenObtainPairView.as_view()),
    path('profile/', profile),
    path('profile/<int:user_id>/', public_profile_details),
    path('users/search/', views.search_user, name='search_user'),
    path('clubs/<int:club_id>/members/', get_club_members),
    path('clubs/<int:club_id>/add-member/', add_member),
    path('promote/', promote_to_leader),
    path('profile/details/', profile_details),
    path('users/<int:user_id>/certificates/', user_certificates),
    path('certificates/', certificate_list),
    path('certificates/<int:pk>/', delete_certificate),
    path('users/<int:user_id>/skills/', user_skills),
    path('skills/', skill_list),
    path('skills/<int:pk>/', delete_skill),
    path('staff/change-password/', StaffChangePasswordView.as_view(), name='staff-change-password'),
    path('staff/search-user/', SearchUserByUniversityIdView.as_view(), name='search-user'),
    path('staff/promote-to-leader/', PromoteToLeaderView.as_view(), name='promote-to-leader'),
    path('students/', views.StudentList),
    path('users/<int:user_id>/posts/', user_posts),
    path('student-posts/<int:post_id>/delete/', views.delete_student_post, name='delete_student_post'),
    path('student-posts/', StudentPostListView.as_view(), name='student-posts-list'),
]