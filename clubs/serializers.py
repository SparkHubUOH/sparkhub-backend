from rest_framework import serializers
from .models import Announcement, Club, ClubPost, Member

class ClubSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Club
        fields = [
            'id', 'club_name', 'club_name_ar', 
            'description', 'description_ar', 
            'status', 'logo', 'created_at', 
            'created_by', 'created_by_name'
        ]
        read_only_fields = ['status', 'created_by', 'created_at']


class MemberSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Member
        fields = [
            'id', 'user', 'club', 'role', 'status', 'joined_at'
        ]
        read_only_fields = ['user', 'club', 'role', 'joined_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'id', 'club', 'title', 'title_ar', 
            'content', 'content_ar', 'is_urgent', 
            'is_pinned', 'created_at'
        ]
        read_only_fields = ['club', 'created_at']
        
        
class ClubPostSerializer(serializers.ModelSerializer):
    club_name = serializers.ReadOnlyField(source='club.club_name')
    class Meta:
        model = ClubPost
        fields = [
            'id', 'club', 'club_name', 'content', 
            'image', 'points_earned', 'created_at'
        ]
        read_only_fields = ['club', 'points_earned', 'created_at']