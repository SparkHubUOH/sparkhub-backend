from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.response import Response

from clubs.serializers import MemberSerializer
from clubs.models import Club, Member
from .models import StudentPost, User, Profile, Certificate, Skill
from .serializers import RegisterSerializer, ProfileSerializer, CertificateSerializer, SkillSerializer, StudentPostSerializer, UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.hashers import check_password
from rest_framework import status

class StaffChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'staff':
            return Response(
                {'error': 'Only staff members can access this endpoint'},
                status=status.HTTP_403_FORBIDDEN
            )

        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not all([current_password, new_password, confirm_password]):
            return Response({'error': 'All fields are required'}, status=400)

        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect'}, status=400)

        if new_password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully'})

class SearchUserByUniversityIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'staff':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_403_FORBIDDEN
            )

        university_id = request.query_params.get('university_id')
        
        if not university_id:
            return Response(
                {'error': 'University ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(university_id=university_id)
            return Response({
                'id': user.id,
                'university_id': user.university_id,
                'full_name': user.get_full_name(),
                'email': user.email,
                'role': user.role
            })
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class PromoteToLeaderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'staff':
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'User ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
            
            if user.role == 'leader':
                return Response(
                    {'error': 'User is already a club leader'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if user.role == 'staff':
                return Response(
                    {'error': 'Cannot change staff role'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.role = 'leader'
            user.save()

            return Response({
                'message': f'{user.get_full_name()} has been promoted to club leader',
                'user': {
                    'id': user.id,
                    'full_name': user.get_full_name(),
                    'role': user.role
                }
            })

        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
            
class StudentPostListView(generics.ListCreateAPIView):
    serializer_class = StudentPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StudentPost.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
              
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
    profile, created = Profile.objects.get_or_create(user=request.user)

    serializer = ProfileSerializer(profile)

    return Response(serializer.data)
    # user = request.user
    # print("PROFILE REQUEST BY:", user.id, user.username)
    
    # return Response({
    #     "first_name": user.first_name,
    #     "last_name": user.last_name,
    #     "email": user.email,
    #     "role": user.role,
    #     "phone": user.phone,
    #     "university_id": user.university_id
    # }) 

@api_view(['GET'])
def search_user(request):
    university_id = request.GET.get('university_id')

    if not university_id:
        return Response({"error": "University ID required"}, status=400)

    try:
        user = User.objects.get(university_id=university_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    serializer = UserSerializer(user)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_member(request, club_id):
    user_id = request.data.get('user_id')
    try:
        club = Club.objects.get(id=club_id)
        user = User.objects.get(id=user_id)
    except:
        return Response({"error": "Invalid club or user"}, status=400)

    member, created = Member.objects.get_or_create(
        user=user,
        club=club,
        defaults={'status': 'accepted', 'role': 'member'}
    )

    if not created:
        return Response({"message": "User already a member"}, status=200)

    return Response({"message": "Member added"}, status=201)

@api_view(['GET'])
def get_club_members(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
    except Club.DoesNotExist:
        return Response({"error": "Club not found"}, status=404)

    members = Member.objects.filter(club=club, status='accepted')
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

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
        user = request.user
        new_email = request.data.get('email', user.email)
        
        user.email = new_email
        user.username = new_email

        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.phone = request.data.get('phone', user.phone)
        user.save()
        
        profile.bio = request.data.get('bio', profile.bio)
        profile.save()
        
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            response_data = serializer.data
            response_data.update({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "bio": profile.bio
            })
            return Response(response_data)
        
        return Response(serializer.errors, status=400)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile_all(request):
    user = request.user
    data = request.data
    
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.phone = data.get('phone', user.phone)
    user.save()
    
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.bio = data.get('bio', profile.bio)
    profile.save()
    
    return Response({"message": "Updated successfully"})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_certificates(request, user_id):
    certificates = Certificate.objects.filter(user_id=user_id)
    serializer = CertificateSerializer(certificates, many=True)
    return Response(serializer.data)
   
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
def user_skills(request, user_id):
    skills = Skill.objects.filter(user_id=user_id)
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)

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

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) 
def user_posts(request, user_id):
    posts = StudentPost.objects.filter(user_id=user_id)
    serializer = StudentPostSerializer(posts, many=True)
    return Response(serializer.data)

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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def StudentList(request):
    students = User.objects.all()
    data = [
        {
            "id": s.id, 
            "username": s.username, 
            "first_name": s.first_name, 
            "last_name": s.last_name, 
            "points": s.points
        } for s in students
    ]
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def public_profile_details(request, user_id):
    profile, created = Profile.objects.get_or_create(user_id=user_id)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)