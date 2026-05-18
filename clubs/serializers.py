from rest_framework import serializers

from .models import Activity, Announcement, Club, ClubPost, Member

class ClubSerializer(serializers.ModelSerializer):
    
    created_by_name = serializers.ReadOnlyField(source='created_by.username')
    first_name = serializers.ReadOnlyField(source='created_by.first_name')
    last_name = serializers.ReadOnlyField(source='created_by.last_name')
    event_count = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    class Meta:
        model = Club
        fields = [
            'id', 'club_name', 'club_name_ar', 
            'description', 'description_ar', 
            'status', 'logo', 'points', 'event_count', 'members_count', 'created_at', 
            'created_by', 'created_by_name', 'first_name', 'last_name'
        ]
        read_only_fields = ['status', 'created_by', 'created_at', 'points']
        
    def get_event_count(self, obj):
        return obj.activities.count()
    
    def get_members_count(self, obj):
        return obj.memberships.filter(status='accepted').count()


class MemberSerializer(serializers.ModelSerializer):   
    full_name = serializers.SerializerMethodField() 
    university_id = serializers.CharField(source='user.university_id', read_only=True)
    club_name = serializers.CharField(source='club.club_name') 
     
    class Meta:
        model = Member
        fields = [
            'id', 'club_name', 'full_name', 'university_id', 
            'user', 'club', 'role', 'team', 'status', 'joined_at'
        ]
        extra_kwargs = {
            'team': {'required': False, 'allow_null': True}
        }
        
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
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
        
        
class ActivitySerializer(serializers.ModelSerializer):
    club_name = serializers.ReadOnlyField(source='club.club_name')
    participants_count = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()
    registeration_points = serializers.ReadOnlyField(source='users.points')

    class Meta:
        model = Activity
        fields = [
            'id', 'club', 'club_name', 'title', 'title_ar', 
            'description', 'description_ar', 'location', 
            'date', 'max_attendees', 'category', 'image',
            'points_to_earn', 'participants_count', 
            'is_registered', 'registeration_points'
        ]
        read_only_fields = ['club']

    def get_participants_count(self, obj):
        return obj.participants.count()

    def get_is_registered(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.participants.filter(id=request.user.id).exists()
        return False