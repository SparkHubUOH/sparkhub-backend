from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import ClubPost, Activity, Announcement, Member

@receiver(post_save, sender=Announcement)
@receiver(post_save, sender=ClubPost)
@receiver(post_save, sender=Activity)
def award_club_points(sender, instance, created, **kwargs):
    if created:
        club = instance.club
        if sender == Announcement:
            club.points += 3
        elif sender == ClubPost:
            club.points += 10
        elif sender == Activity:
            club.points += 15 
        club.save()

@receiver(post_save, sender=Member)
def award_points_for_new_member(sender, instance, created, **kwargs):
    if instance.status == 'accepted':
        club = instance.club
        club.points += 1
        club.save()

@receiver(m2m_changed, sender=Activity.participants.through)
def award_points_for_activity_join(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        from users.models import User
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            user.points += 3
            user.save()