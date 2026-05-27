import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
from clubs.models import Club, Member 

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            cyber_club = Club.objects.get(
                Q(club_name__icontains='Cyber') | Q(club_name_ar__icontains='السيبراني')
            )
        except Club.DoesNotExist:
            self.stdout.write(self.style.ERROR('SQL error: Cyber Club not found. Please create the club first and then run this command.'))
            return

        members_data = [
            # القيادة
            {'first': 'Majed', 'last': 'Alshammari', 'team': 'management', 'm_role': 'team leader'},
            {'first': 'Manar', 'last': 'Almutairi', 'team': 'management', 'm_role': 'vice leader'},
            
            # فريق الإدارة
            {'first': 'Omran', 'last': 'Alselimi', 'team': 'management', 'm_role': 'team leader'},
            {'first': 'Ohood', 'last': 'Alharbi', 'team': 'management', 'm_role': 'vice leader'},
            {'first': 'Fan', 'last': 'Alshuhail', 'team': 'management', 'm_role': 'member'},
            {'first': 'Raghad', 'last': 'Alharbi', 'team': 'management', 'm_role': 'member'},
            {'first': 'Haneen', 'last': 'Alharbi', 'team': 'management', 'm_role': 'member'},
            {'first': 'Nawaf', 'last': 'Alenezi', 'team': 'management', 'm_role': 'member'},
            {'first': 'Raad', 'last': 'Almuqtiran', 'team': 'management', 'm_role': 'member'},
            {'first': 'Raseel', 'last': 'Alenezi', 'team': 'management', 'm_role': 'member'},

            # فريق التصميم
            {'first': 'Alaa', 'last': 'Alhuthayris', 'team': 'design', 'm_role': 'team leader'},
            {'first': 'Moath', 'last': 'Alharbi', 'team': 'design', 'm_role': 'vice leader'},
            {'first': 'Joud', 'last': 'Alhudaibi', 'team': 'design', 'm_role': 'member'},
            {'first': 'Ghareeba', 'last': 'Alshuqair', 'team': 'design', 'm_role': 'member'},
            {'first': 'Mala', 'last': 'Alshammari', 'team': 'design', 'm_role': 'member'},
            {'first': 'Leena', 'last': 'Alqahtani', 'team': 'design', 'm_role': 'member'},
            {'first': 'Reem', 'last': 'Alharbi', 'team': 'design', 'm_role': 'member'},

            # فريق المحتوى
            {'first': 'Wala', 'last': 'Alenezi', 'team': 'content', 'm_role': 'team leader'},
            {'first': 'Hiyam', 'last': 'Alenezi', 'team': 'content', 'm_role': 'vice leader'},
            {'first': 'Sahar', 'last': 'Altabob', 'team': 'content', 'm_role': 'member'},
            {'first': 'Ashwaq', 'last': 'Alnowmsi', 'team': 'content', 'm_role': 'member'},
            
            # فريق المشاريع/CyberWings
            {'first': 'Fares', 'last': 'Almutairi', 'team': 'projects', 'm_role': 'team leader'},
            {'first': 'Sawsan', 'last': 'Aljarallah', 'team': 'projects', 'm_role': 'vice leader'},
            {'first': 'Rashid', 'last': 'Alamro', 'team': 'projects', 'm_role': 'member'},
            {'first': 'Alanoud', 'last': 'Alshammari', 'team': 'projects', 'm_role': 'member'},
            {'first': 'Abdurahman', 'last': 'Alhayah', 'team': 'projects', 'm_role': 'member'},

            # فريق الفعاليات
            {'first': 'Shaden', 'last': 'Alenezi', 'team': 'events', 'm_role': 'team leader'},
            {'first': 'Abdullah', 'last': 'Alhujaili', 'team': 'events', 'm_role': 'vice leader'},
            {'first': 'Aseel', 'last': 'Alfreidi', 'team': 'events', 'm_role': 'member'},
            {'first': 'Lama', 'last': 'Alshammari', 'team': 'events', 'm_role': 'member'},

            # فريق الإعلام
            {'first': 'Nouf', 'last': 'Alenezi', 'team': 'media', 'm_role': 'team leader'},
            {'first': 'Shahad', 'last': 'Alshammari', 'team': 'media', 'm_role': 'vice leader'},
            {'first': 'Lamees', 'last': 'Mufreh', 'team': 'media', 'm_role': 'member'},
            {'first': 'Amira', 'last': 'Alhamzani', 'team': 'media', 'm_role': 'member'},
        ]

        success_count = 0
        for data in members_data:
            username = f"{data['first'][:3].lower()}_{random.randint(100, 999)}"
            
            while User.objects.filter(username=username).exists():
                username = f"{data['first'][:3].lower()}_{random.randint(100, 999)}"

            user = User.objects.create(
                username=f"{username}@gmail.com",
                first_name=data['first'],
                last_name=data['last'],
                email=f"{username}@gmail.com",
                role='student',
                phone="05" + "".join([str(random.randint(0, 9)) for _ in range(8)]),
                university_id="202" + "".join([str(random.randint(0, 9)) for _ in range(6)]),
                points=random.randint(20, 100),
                is_active=True
            )
            user.set_password('SparkHub2026$')
            user.save()

            Member.objects.create(
                user=user,
                club=cyber_club,
                team=data['team'],
                role=data['m_role'],
                status='accepted'
            )
            success_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {success_count} students and linked to Club!'))