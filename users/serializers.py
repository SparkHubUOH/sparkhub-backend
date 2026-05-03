from rest_framework import serializers
from .models import User, Profile, Certificate, Skill

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
    
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio']
   
        
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['id', 'name', 'date']
        
        
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']