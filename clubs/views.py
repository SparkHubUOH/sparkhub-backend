from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q, Count
from users.models import User
from rest_framework import status
from .models import Activity, Announcement, Club, ClubPost, Member
from .serializers import ActivitySerializer, AnnouncementSerializer, ClubPostSerializer, ClubSerializer
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

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

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def club_detail(request, pk):
    try:
        club = Club.objects.get(pk=pk)
    except Club.DoesNotExist:
        return Response(
            {'error': 'Club not found.'},
            status=404
        )

    if request.method == 'GET':
        serializer = ClubSerializer(club)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        print(request.data)

        serializer = ClubSerializer(
            club,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        print(serializer.errors)
        return Response(serializer.errors, status=400)
             
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_club_posts(request, club_id):
    try:
        posts = ClubPost.objects.filter(club_id=club_id).order_by('-created_at')

        serializer = ClubPostSerializer(posts, many=True)

        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def ClubList(request):
    clubs = Club.objects.all()
    data = [
    {
        'id': club.id,
        'club_name': club.club_name,      
        'club_name_ar': club.club_name_ar, 
        'description': club.description,
        'description_ar': club.description_ar,
        'points': club.points,          
        'status': club.status,
        'logo': club.logo.url if club.logo else None
    }
        for club in clubs
    ]
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_club(request):
    try:
        club = Club.objects.get (
        created_by=request.user,
        status='active'
        ) 
        return Response({'id': club.id})
    except Club.DoesNotExist:
        return Response({'error': 'No club found for this leader'}, status=404)

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_join_requests(request, club_id):
    try:
        club = Club.objects.get(id=club_id)

        if club.created_by != request.user:
            return Response({'error': 'Not authorized'}, status=403)

        pending_members = Member.objects.filter(club=club, status='pending')

        data = [
            {
                'id': m.id,
                'full_name': f"{m.user.first_name} {m.user.last_name}",
                'university_id': m.user.university_id,
                'user': {'id': m.user.id},
                'status': m.status,
            }
            for m in pending_members
        ]

        return Response(data, status=200)

    except Club.DoesNotExist:
        return Response({'error': 'Club not found'}, status=404)

  
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
 
 
 # في views.py (الدالة التي ترجع قائمة الأعضاء)
def get_club_members(request, club_id):
    members = Member.objects.filter(club_id=club_id, status='accepted')\
                            .select_related('user')\
                            .only('id', 'role', 'team', 'user__first_name', 'user__last_name', 'user__id')
    
    data = [{
        "id": m.id,
        "role": m.role,
        "full_name": f"{m.user.first_name} {m.user.last_name}",
        "user": m.user.id,
        "team": m.team
    } for m in members]
    
    return Response(data)
   
    
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


@api_view(['DELETE'])
def delete_member(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
        
        member.delete()
        
        return Response({"message": "Member deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    except Member.DoesNotExist:
        return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrgChartView(APIView):
    def get(self, request, club_id):
        
        try:
            club = Club.objects.select_related('created_by').get(id=club_id)
        except Club.DoesNotExist:
            return Response({"error": "Club not found"}, status=404)
        
        all_members = Member.objects.filter(
            club_id=club_id, 
            status='accepted'
        ).select_related('user').order_by('team')
        
        club_leader = f"{club.created_by.first_name} {club.created_by.last_name}"
        vice_leader_obj = all_members.filter(role='vice leader').filter(Q(team__isnull=True) | Q(team='')).first()
        
        teams_dict = {}
        for m in all_members:
            if not m.team: continue
            
            if m.team not in teams_dict:
                teams_dict[m.team] = {"name": m.team, "teamLeader": "TBD", "viceLeader": "TBD", "members": []}
            
            full_name = m.user.get_full_name()
            if m.role == 'team leader':
                teams_dict[m.team]["teamLeader"] = full_name
            elif m.role == 'vice leader':
                teams_dict[m.team]["viceLeader"] = full_name
            elif m.role == 'member':
                teams_dict[m.team]["members"].append(full_name)

        return Response({
            "clubLeader": club_leader,
            "clubViceLeader": vice_leader_obj.user.get_full_name() if vice_leader_obj else "",
            "teams": list(teams_dict.values())
        })


class UpdateMemberRoleView(APIView):
    def post(self, request):
        member_id = request.data.get('member_id')
        new_role = request.data.get('role') 
        new_team = request.data.get('team') 
        
        try:
            member = Member.objects.get(id=member_id)
            member.role = new_role
            member.team = new_team
            member.status = 'accepted'
            member.save()
            return Response({"message": "تم تحديث الدور بنجاح"})
        except Member.DoesNotExist:
            return Response({"error": "العضو غير موجود"}, status=404)
        

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
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_club_post(request, post_id):
    try:
        post = ClubPost.objects.get(id=post_id)
        
        if post.club.created_by != request.user:
            return Response({"error": "You don't have permission to delete this post."}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    except ClubPost.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def activity_list_create(request, club_id):
    try:
        club = Club.objects.get(id=club_id)
        
        if request.method == 'GET':
            activities = club.activities.all().order_by('date')
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response(serializer.data)

        if request.method == 'POST':
            if club.created_by != request.user:
                return Response({'error': 'Only club leader can create activities.'}, status=403)
            
            serializer = ActivitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(club=club)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
            
    except Club.DoesNotExist:
        return Response({'error': 'Club not found.'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_activity(request, pk):
    try:
        activity = Activity.objects.get(pk=pk)
        activity.delete()
        
        return Response({'message': 'Activity deleted successfully'}, status=200)
    
    except Activity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


class ActivityPagination(PageNumberPagination):
    page_size = 20
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_activities_list(request):
    try:
        activities = Activity.objects.select_related('club')\
                             .annotate(participants_count=Count('participants'))\
                             .all().order_by('date')

        data = []
        for act in activities:
            data.append({
                "id": act.id,
                "title": act.title,
                "title_ar": act.title_ar,
                "description": act.description,
                "location": act.location,
                "date": act.date.isoformat(),
                "max_attendees": act.max_attendees,
                "category": act.category,
                "image": request.build_absolute_uri(act.image.url) if act.image else None,
                "points_to_earn": act.points_to_earn,
                "club_name": act.club.club_name, 
                "participants_count": act.participants_count,
            })
        
        return Response(data)
    except Exception as e:
        print(f"Error in activities list: {e}")
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_for_activity(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
        
        if activity.participants.filter(id=request.user.id).exists():
            return Response({'message': 'You are already registered.'}, status=400)
        
        if activity.participants.count() >= activity.max_attendees:
            return Response({'error': 'Activity is full.'}, status=400)
        
        activity.participants.add(request.user)
        activity.save()
        return Response({'message': 'Registered successfully.'}, status=200)
        
    except Activity.DoesNotExist:
        return Response({'error': 'Activity not found.'}, status=404)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def registered_activities_list(request):
    activities = request.user.attended_activities.all().order_by('-date')
    serializer = ActivitySerializer(activities, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_activity_participants(request, activity_id):
    try:
        
        activity = Activity.objects.get(pk=activity_id)
        participants = activity.participants.all() 
        
        data = []
        for user in participants:
            data.append({
                'userId': user.id,
                'name': f"{user.first_name} {user.last_name}" if user.first_name else user.username,
                'email': user.email,
                'university_id': getattr(user, 'university_id', 'N/A'),
                'role': user.role 
            })
            
        return Response({
            'activity_title': activity.title,
            'participants': data
        }, status=200)

    except Activity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=404)
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_participant_from_activity(request, activity_id, user_id):
    try:
        activity = Activity.objects.get(pk=activity_id)
        participant = activity.participants.get(id=user_id)
        
        activity.participants.remove(participant)
        
        return Response({'message': 'Participant removed successfully'}, status=200)
    except (Activity.DoesNotExist, User.DoesNotExist):
        return Response({'error': 'Not found'}, status=404)