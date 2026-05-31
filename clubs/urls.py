from django.urls import path
from . import views

urlpatterns = [
    path('clubs/', views.club_list_create),
    path('clubs/<int:pk>/', views.club_detail),
    path('clubs/list/', views.ClubList),
    path('clubs/my-club/', views.get_my_club),
    path('clubs/<int:pk>/approve/', views.approve_club),
    path('clubs/<int:club_id>/join-requests/', views.get_join_requests),
    path('clubs/<int:club_id>/join/', views.join_club),
    path('clubs/<int:member_id>/manage/', views.manage_member),
    path('members/<int:member_id>/', views.delete_member, name='delete_member'),
    path('clubs/<int:club_id>/org-chart/', views.OrgChartView.as_view(), name='org-chart'),
    path('update-member-role/', views.UpdateMemberRoleView.as_view(), name='update-member-role'),
    path('clubs/<int:club_id>/announcements/', views.get_announcements), 
    path('clubs/<int:club_id>/announcements/create/', views.create_announcement),
    path('posts/', views.get_all_posts), 
    path('clubs/<int:club_id>/posts/', views.get_club_posts),
    path('clubs/<int:club_id>/posts/create/', views.create_club_post),
    path('posts/<int:post_id>/delete/', views.delete_club_post, name='delete_club_post'),
    path('clubs/<int:club_id>/activities/', views.activity_list_create),
    path('activities/<int:pk>/delete/', views.delete_activity),
    path('activities/all/', views.all_activities_list),
    path('activities/<int:activity_id>/register/', views.register_for_activity),
    path('activities/my-activities/', views.registered_activities_list),
    path('activities/<int:activity_id>/participants/', views.get_activity_participants),
    path('activities/<int:activity_id>/participants/<int:user_id>/remove/', views.remove_participant_from_activity),
]