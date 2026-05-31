import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clubs.models import Club, Member

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with Programming and Games Club (PG Club) data'

    def handle(self, *args, **options):
        target_club_name = "PG Club"
        creator_email = "abd222@gmail.com"
        
        creator_user = User.objects.filter(email=creator_email).first()
        if not creator_user:
            self.stdout.write(self.style.ERROR(f'Creator user {creator_email} not found!'))
            return

        club, created = Club.objects.get_or_create(
            club_name=target_club_name,
            defaults={'created_by': creator_user, 'club_name_ar': 'نادي البرمجة والألعاب'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new club: {target_club_name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Using existing club: {target_club_name}'))

        data = {
            'leaders': [
                {'name': 'Jouri Alshammari', 'role': 'leader'},
                {'name': 'Saud Alasal', 'role': 'vice leader'},
            ],
            'design': [
                {'name': 'Sahar Alshammari', 'role': 'team leader'},
                {'name': 'Lujain Al-Tamimi', 'role': 'member'},
                {'name': 'Sarah Al-Ghaffan', 'role': 'member'},
                {'name': 'Rawan Al-Rashidi', 'role': 'member'},
                {'name': 'Latifah Al-Eid', 'role': 'member'},
                {'name': 'Fi Al-Tamimi', 'role': 'member'},
                {'name': 'Jauhara Al-Mushari', 'role': 'member'},
                {'name': 'Raad Al-Qalladi', 'role': 'member'},
                {'name': 'Layan Al-Jaser', 'role': 'member'},
                {'name': 'Hala Al-Gharifi', 'role': 'member'},
                {'name': 'Madawi Ahmed', 'role': 'member'},
                {'name': 'Salwa Al-Sulaimi', 'role': 'member'},
                {'name': 'Shahad Bandar', 'role': 'member'},
                {'name': 'Reef Al-Barrak', 'role': 'member'},
            ],
            'media': [
                {'name': 'Mashael Al-Obaiekel', 'role': 'team leader'},
                {'name': 'Mohammed Al-Nasser', 'role': 'vice leader'},
                {'name': 'Renim Alkhuraif', 'role': 'member'},
                {'name': 'Omar Al-Dihani', 'role': 'member'},
                {'name': 'Hadeel Hammad', 'role': 'member'},
                {'name': 'Nouf Marzi', 'role': 'member'},
                {'name': 'Ruba Sultan', 'role': 'member'},
                {'name': 'Arwa Alrashidi', 'role': 'member'},
                {'name': 'Khulood Alshammari', 'role': 'member'},
            ],
            'organization': [
                {'name': 'Noura Almujahid', 'role': 'team leader'},
                {'name': 'Talal Alduhailan', 'role': 'vice leader'},
                {'name': 'Alanoud Almujahid', 'role': 'member'},
                {'name': 'Shouq Alqanoon', 'role': 'member'},
                {'name': 'Raghad Alshammari', 'role': 'member'},
                {'name': 'Latifah Aldhamadi', 'role': 'member'},
                {'name': 'Ammar Alshammari', 'role': 'member'},
                {'name': 'Retaj Alharbi', 'role': 'member'},
                {'name': 'Dhi Almutaib', 'role': 'member'},
                {'name': 'Rayat Al-Nasser Allah', 'role': 'member'},
                {'name': 'Noura Almujahid', 'role': 'member'},
                {'name': 'Ola Aljarbou', 'role': 'member'},
                {'name': 'Nouf Alrashidi', 'role': 'member'},
                {'name': 'Layan Alshammari', 'role': 'member'},
                {'name': 'Sari Alshammari', 'role': 'member'},
                {'name': 'Mohammed Hashem', 'role': 'member'},
                {'name': 'Ziyad Waleed', 'role': 'member'},
                {'name': 'Abdulmalik Alshammari', 'role': 'member'},
                {'name': 'Abdullah Alshammari', 'role': 'member'},
                {'name': 'Musa Al-Ghaffan', 'role': 'member'},
                {'name': 'Mansour Al-Anzi', 'role': 'member'},
            ],
            'projects': [
                {'name': 'Majed Alabdali', 'role': 'team leader'},
                {'name': 'Sheikha Alomair', 'role': 'vice leader'},
                {'name': 'Munira Al-Jabr', 'role': 'member'},
                {'name': 'Rimas Al-Anzi', 'role': 'member'},
                {'name': 'Hasana Alharbi', 'role': 'member'},
                {'name': 'Amjad Hamad', 'role': 'member'},
                {'name': 'Jouri Alshammari', 'role': 'member'},
                {'name': 'Reef Alshammari', 'role': 'member'},
                {'name': 'Mashael Al-Anzi', 'role': 'member'},
                {'name': 'Atheer Al-Anzi', 'role': 'member'},
                {'name': 'Arwa Alrashidi', 'role': 'member'},
                {'name': 'Hamad Al-Mushari', 'role': 'member'},
                {'name': 'Amira Shaya', 'role': 'member'},
                {'name': 'Dana Al-Anzi', 'role': 'member'},
                {'name': 'Ali Al-Qanoon', 'role': 'member'},
                {'name': 'Anas Alshammari', 'role': 'member'},
                {'name': 'Ziyad Alshammari', 'role': 'member'},
            ],
            'content': [
                {'name': 'Sadeem Al-Hamoud', 'role': 'team leader'},
                {'name': 'Layan Al-Seryati', 'role': 'member'},
                {'name': 'Dhi Al-Tamimi', 'role': 'member'},
                {'name': 'Faiza Al-Juraib', 'role': 'member'},
                {'name': 'Nahla Alfaraj', 'role': 'member'},
                {'name': 'Moudi Alshammari', 'role': 'member'},
                {'name': 'Noha Alshammari', 'role': 'member'},
            ]
        }

        success_count = 0
        for team_name, members in data.items():
            for m in members:
                full_name_parts = m['name'].split()
                first = full_name_parts[0]
                last = full_name_parts[-1] if len(full_name_parts) > 1 else "User"
                
                clean_username = f"{first[:3].lower()}{random.randint(1000, 9999)}"
                email = f"{clean_username}@gmail.com"

                user, user_created = User.objects.get_or_create(
                    first_name=first,
                    last_name=last,
                    defaults={
                        'username': email,
                        'email': email,
                        'role': 'student',
                        'phone': "05" + "".join([str(random.randint(0, 9)) for _ in range(8)]),
                        'university_id': "202" + "".join([str(random.randint(0, 9)) for _ in range(6)]),
                        'points': random.randint(20, 100),
                        'is_active': True
                    }
                )

                if user_created:
                    user.set_password('SparkHub2026$')
                    user.save()

                Member.objects.get_or_create(
                    user=user,
                    club=club,
                    defaults={
                        'team': team_name,
                        'role': m['role'],
                        'status': 'accepted'
                    }
                )
                success_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {success_count} members for PG Club! ✅'))