from rest_framework import serializers
from django.db.models import Q
from clubs.models import Club
from .models import StudentPost, User, Profile, Certificate, Skill

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'phone',
            'university_id'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
   
    def create(self, validated_data):
        password = validated_data.pop('password')

        if not validated_data.get('username'):
            validated_data['username'] = validated_data.get('email')
        
        user = User(**validated_data)
        user.role = 'student'
        user.set_password(password)
        user.save()

        return user
   
   
class UserSerializer(serializers.ModelSerializer):
    created_club = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    def get_created_club(self, obj):
        club = Club.objects.filter(created_by=obj).first()
        if club:
            return {
                "id": club.id,
                "club_name": club.club_name
            }
        return None

    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'university_id', 'created_club', 'full_name']

        
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'name', 'date']
        
        
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        
        
class StudentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPost
        fields = ['id', 'content', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']
        
        
class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    points = serializers.IntegerField(source='user.points', read_only=True)
    role = serializers.ReadOnlyField(source='user.role')
    skills = SkillSerializer(many=True, read_only=True)
    certificates = CertificateSerializer(many=True, read_only=True)
    clubs = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id','bio', 'first_name', 'last_name', 
        'email', 'phone', 'role', 'points', 'skills', 
        'certificates', 'clubs']
        
        
    def get_clubs(self, obj):
        user = obj.user
        all_user_clubs = []
        owned_clubs = Club.objects.filter(created_by=user, status='active')
        for club in owned_clubs:
            all_user_clubs.append({
            'id': club.id,
            'club_name': club.club_name,
            'logo': club.logo.url if club.logo else None,
            'membership_status': 'accepted',
            'club_status': club.status,
            'role': 'team leader',
            'is_leader': True 
           })

        memberships = obj.user.memberships.filter(
            Q(status='accepted') | Q(role__in=['team leader', 'vice leader']),
            club__status='active'
        ).distinct()
        
        for m in memberships:
            if not any(c['id'] == m.club.id for c in all_user_clubs):
                all_user_clubs.append({
                'id': m.club.id,
                'club_name': m.club.club_name,
                'logo': m.club.logo.url if m.club.logo else None,
                'membership_status': m.status,
                'club_status': m.club.status,
                'role': m.role,
                'is_leader': False
                })

        return all_user_clubs