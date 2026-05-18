from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Certificate, Skill, StudentPost
from clubs.models import ClubPost

@receiver(post_save, sender=Certificate)
def award_points_for_certificate(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.points += 5
        user.save()

@receiver(post_save, sender=Skill)
def award_points_for_skill(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.points += 2
        user.save()
        
@receiver(post_save, sender=StudentPost)
def award_points_for_student_post(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.points += 10
        user.save()

@receiver(post_save, sender=ClubPost)
def award_points_for_post(sender, instance, created, **kwargs):
    if created:
        club = instance.club
        club.points += 10
        club.save()