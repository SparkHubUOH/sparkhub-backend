from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from clubs.models import Club
from .models import User, Profile, Certificate, Skill
from .serializers import RegisterSerializer, ProfileSerializer, CertificateSerializer, SkillSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def register(request):
    print("DATA:",request.data)
    
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        print("USER CREATED:", user.id, user.username)
        return Response({'message': 'User created successfully'})
    else:
        print("SERIALIZER ERRORS:", serializer.errors)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@authentication_classes([JWTAuthentication]) 
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    print("PROFILE REQUEST BY:", user.id, user.username)
    
    return Response({
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,
        "phone": user.phone,
        "university_id": user.university_id
    })
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def promote_to_leader(request):
    if request.user.role != 'staff':
        return Response({'error': 'Unauthorized'}, status=403)

    university_id = request.data.get('university_id')

    try:
        user = User.objects.get(university_id=university_id)
        user.role = 'leader'
        user.save()

        return Response({'message': 'User promoted to leader'})
    
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_details(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def certificate_list(request):
    if request.method == 'GET':
        certificates = Certificate.objects.filter(user=request.user)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CertificateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_certificate(request, pk):
    try:
        certificate = Certificate.objects.get(pk=pk, user=request.user)
        certificate.delete()
        return Response({'message': 'Certificate deleted successfully'}, status=204)
    except Certificate.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def skill_list(request):
    if request.method == 'GET':
        skills = Skill.objects.filter(user=request.user)
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_skill(request, pk):
    try:
        skill = Skill.objects.get(pk=pk, user=request.user)
        skill.delete()
        return Response({'message': 'Skill deleted successfully'}, status=204)
    except Skill.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_leaderboard(request):
    top_students = User.objects.order_by('-points')[:3]
    top_clubs = Club.objects.order_by('-points')[:3]
    
    return Response({
        "students": [
            {"username": s.username, "points": s.points} for s in top_students
        ],
        "clubs": [
            {"name": c.club_name, "points": c.points} for c in top_clubs
        ]
    })