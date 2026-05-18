from django.db import models
from django.conf import settings

class Club(models.Model):
    STATUS_CHOICES = [
        ('active', 'نشط'),
        ('inactive', 'غير نشط'),
        ('pending', 'قيد الانتظار'),
    ]

    club_name = models.CharField(max_length=255, unique=True)
    description = models.TextField() 
    
    club_name_ar = models.CharField(max_length=255, unique=True, null=True, blank=True)
    description_ar = models.TextField(null=True, blank=True)
    
    points = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    logo = models.ImageField(upload_to='club_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True
    )

    def __str__(self):
        return self.club_name
    
class Member(models.Model):
    ROLE_CHOICES = [
        ('member', 'عضو'),
        ('team leader', 'قائد الفريق'),
        ('vice leader', 'نائب القائد')
    ]
    
    TEAM_CHOICES = [
    ('events', 'Events'),
    ('media', 'Media'),
    ('design', 'Design'),
    ('content', 'Content'),
    ('projects', 'Projects'),
    ('management', 'Management'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    team = models.CharField(max_length=30, choices=TEAM_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'club') 

    def __str__(self):
        return f"{self.user.username} in {self.club.club_name}"
    
class Announcement(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    content_ar = models.TextField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{' [URGENT] ' if self.is_urgent else ''}{self.title}"
    
class ClubPost(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='club_posts/', null=True, blank=True)
    points_earned = models.IntegerField(default=10) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.club.club_name} at {self.created_at}"
    
class Activity(models.Model):
    CATEGORY_CHOICES = [
        ('WORKSHOPS', 'Workshops'),
        ('DISCUSSIONS', 'Discussions'),
        ('EXHIBITIONS', 'Exhibitions'),
        ('OTHER', 'Other'),
    ]
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    description_ar = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    max_attendees = models.IntegerField(default=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    image = models.ImageField(upload_to='activities/', null=True, blank=True)
    points_to_earn = models.IntegerField(default=15)
    
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attended_activities', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title