from django.urls import path
from . import views

urlpatterns = [
    path('clubs/', views.club_list_create),
    path('clubs/<int:pk>/approve/', views.approve_club),
    path('clubs/<int:club_id>/join/', views.join_club),
    path('clubs/<int:member_id>/manage/', views.manage_member),
    path('clubs/<int:club_id>/announcements/', views.get_announcements), 
    path('clubs/<int:club_id>/announcements/create/', views.create_announcement),
    path('posts/', views.get_all_posts), 
    path('clubs/<int:club_id>/posts/create/', views.create_club_post),
]