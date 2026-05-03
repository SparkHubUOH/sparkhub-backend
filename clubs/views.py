from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Announcement, Club, ClubPost, Member
from .serializers import AnnouncementSerializer, ClubPostSerializer, ClubSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def club_list_create(request):
    if request.method == 'GET':
        if request.user.role == 'staff':
            clubs = Club.objects.all()
        else:
            clubs = Club.objects.filter(status='active')
        
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if request.user.role != 'leader':
            return Response({'error': 'only leaders can submit a new club request.'}, status=403)
        
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response({'message': 'Club request submitted successfully.'}, status=201)
        return Response(serializer.errors, status=400)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def approve_club(request, pk):
    if request.user.role != 'staff':
        return Response({'error': 'only staff members can approve club requests.'}, status=403)

    try:
        club = Club.objects.get(pk=pk)
        action = request.data.get('action') 

        if action == 'approve':
            club.status = 'active'
            club.save()
            return Response({'message': f'Club {club.club_name} approved successfully.'})
        
        elif action == 'reject':
            club.status = 'inactive'
            club.save()
            return Response({'message': f'Club {club.club_name} rejected successfully.'})
        
        return Response({'error': 'Invalid action.'}, status=400)

    except Club.DoesNotExist:
        return Response({'error': 'Club not found.'}, status=404)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_club(request, club_id):
    try:
        club = Club.objects.get(id=club_id, status='active')
        
        member, created = Member.objects.get_or_create(user=request.user, club=club)
        
        if not created:
            return Response({'message': 'You have already sent a request to this club.'}, status=400)
            
        return Response({'message': 'Join request sent successfully.'}, status=201)
        
    except Club.DoesNotExist:
        return Response({'error': 'Club not found or not active.'}, status=404)
    
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def manage_member(request, member_id):
    try:
        member_request = Member.objects.get(id=member_id)
        if member_request.club.created_by != request.user:
            return Response({'error': 'Only the club leader can manage members.'}, status=403)

        action = request.data.get('action')
        if action == 'accept':
            member_request.status = 'accepted'
            member_request.save()
            return Response({'message': 'Member accepted.'})
        elif action == 'reject':
            member_request.status = 'rejected'
            member_request.save()
            return Response({'message': 'Member rejected.'})

    except Member.DoesNotExist:
        return Response({'error': 'Request not found.'}, status=404)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_announcements(request, club_id):
    try:
        announcements = Announcement.objects.filter(club_id=club_id).order_by('-is_pinned', '-created_at')
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_announcement(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
        
        if club.created_by != request.user:
            return Response({'error': 'Only the club leader can post announcements.'}, status=403)
        
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(club=club)
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
        
    except Club.DoesNotExist:
        return Response({'error': 'Club not found.'}, status=404)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    posts = ClubPost.objects.all().order_by('-created_at')
    serializer = ClubPostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_club_post(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
        
        if club.created_by != request.user:
            return Response({'error': 'Only the club leader can create posts.'}, status=403)
        
        serializer = ClubPostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(club=club)
            
            club.points += post.points_earned
            club.save()
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
    except Club.DoesNotExist:
        return Response({'error': 'Club not found.'}, status=404)