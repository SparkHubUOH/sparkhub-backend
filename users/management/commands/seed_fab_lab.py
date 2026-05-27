import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clubs.models import Club, Member 

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with FAB LAB CLUB data using correct field names'

    def handle(self, *args, **options):
        target_club_name = "FAB LAB CLUB"
        creator_email = "ham_933@gmail.com"
        
        creator_user = User.objects.filter(email=creator_email).first()
        if not creator_user:
            self.stdout.write(self.style.ERROR(f'Creator user {creator_email} not found!'))
            return

        club, created = Club.objects.get_or_create(
            club_name=target_club_name,
            defaults={'created_by': creator_user}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created new club: {target_club_name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Using existing club: {target_club_name}'))

        data = {
            'content': [
                {'name': 'Hiyam Alenezi', 'role': 'team leader'},
                {'name': 'Wala Alenezi', 'role': 'member'},
                {'name': 'Arwa Alshammari', 'role': 'member'},
                {'name': 'Nahla Alfaraj', 'role': 'member'},
                {'name': 'Ahdab Almuzaini', 'role': 'member'},
                {'name': 'Shurooq Alhamzani', 'role': 'member'},
                {'name': 'Alhanouf', 'role': 'member'},
                {'name': 'Alia Altuwala', 'role': 'member'},
            ],
            'projects': [
                {'name': 'Abdulmajeed Alshammari', 'role': 'team leader'},
                {'name': 'Sheikha Alomair', 'role': 'vice leader'},
                {'name': 'Salma Alghasham', 'role': 'member'},
                {'name': 'Rima Alrashidi', 'role': 'member'},
                {'name': 'Renad Alsagri', 'role': 'member'},
                {'name': 'Rima Albejadi', 'role': 'member'},
                {'name': 'Hayat Fahem', 'role': 'member'},
                {'name': 'Rima Alomari', 'role': 'member'},
                {'name': 'Rahaf Aldhamadi', 'role': 'member'},
                {'name': 'Shahad Alshammari', 'role': 'member'},
                {'name': 'Saba Albejadi', 'role': 'member'},
                {'name': 'Kadi Alharbi', 'role': 'member'},
                {'name': 'Amjad Alshammari', 'role': 'member'},
                {'name': 'Atheer Al-Tamimi', 'role': 'member'},
                {'name': 'Rimas Alenezi', 'role': 'member'},
                {'name': 'Mashael Alenezi', 'role': 'member'},
                {'name': 'Shaden Alkhurais', 'role': 'member'},
                {'name': 'Milaf Alshammari', 'role': 'member'},
                {'name': 'Sarah Alrashidi', 'role': 'member'},
                {'name': 'Noura Alamro', 'role': 'member'},
                {'name': 'Arene Alfaqih', 'role': 'member'},
                {'name': 'Nuha Alshammari', 'role': 'member'},
                {'name': 'Basma Alenezi', 'role': 'member'},
                {'name': 'Hamoud Almujahid', 'role': 'member'},
                {'name': 'Reham Alolayan', 'role': 'member'},
                {'name': 'Mahmoud Lutfi', 'role': 'member'},
                {'name': 'Raghad Alshammari', 'role': 'member'},
                {'name': 'Abdulaziz Alatiwi', 'role': 'member'},
                {'name': 'Abdullah Alnuzha', 'role': 'member'},
                {'name': 'Maram Alshammari', 'role': 'member'},
                {'name': 'Abdullah Alkhumshi', 'role': 'member'},
                {'name': 'Bassam Alshammari', 'role': 'member'},
                {'name': 'Aseel Alrashidi', 'role': 'member'},
                {'name': 'Farah Alshammari', 'role': 'member'},
                {'name': 'Shaden Almurayziq', 'role': 'member'},
                {'name': 'Jana Aljunaidi', 'role': 'member'},
                {'name': 'Aryam Alazmi', 'role': 'member'},
                {'name': 'Ayat Aljunaidi', 'role': 'member'},
                {'name': 'Dalia Alshammari', 'role': 'member'},
                {'name': 'Talal Alqasim', 'role': 'member'},
                {'name': 'Haneen Alenezi', 'role': 'member'},
                {'name': 'Abdullah Alhujailli', 'role': 'member'},
                {'name': 'Osama Alhuwawi', 'role': 'member'},
                {'name': 'Jumana Alharbi', 'role': 'member'},
                {'name': 'Di Mohammed', 'role': 'member'},
            ],
            'design': [
                {'name': 'Reham Alolayan', 'role': 'team leader'},
                {'name': 'Sahar Hammad', 'role': 'vice leader'},
                {'name': 'Nouf Alrashidi', 'role': 'member'},
                {'name': 'Joud Aljudaie', 'role': 'member'},
                {'name': 'Reem Alharbi', 'role': 'member'},
                {'name': 'Farah Alshammari', 'role': 'member'},
                {'name': 'Raghad Alshammari', 'role': 'member'},
                {'name': 'Heba Almurshid', 'role': 'member'},
                {'name': 'Sawsan Member', 'role': 'member'},
                {'name': 'Shatha Member', 'role': 'member'},
                {'name': 'Al-Anoud Alsiryati', 'role': 'member'},
                {'name': 'Alaa Alhudaybi', 'role': 'member'},
                {'name': 'Shoq Alqanoon', 'role': 'member'},
            ],
            'media': [
                {'name': 'Mohammed Alharbi', 'role': 'team leader'},
                {'name': 'Mashael Alanezi', 'role': 'vice leader'},
                {'name': 'Mohannad Alshammari', 'role': 'member'},
                {'name': 'Abdullah Alali', 'role': 'member'},
                {'name': 'Fatimah Ahmed', 'role': 'member'},
                {'name': 'Raghad Saud', 'role': 'member'},
                {'name': 'Elaf Mohammed', 'role': 'member'},
                {'name': 'Faisal Khalid', 'role': 'member'},
                {'name': 'Hadeel Abdullah', 'role': 'member'},
                {'name': 'Nasser Alshammari', 'role': 'member'},
                {'name': 'Rawan Alali', 'role': 'member'},
                {'name': 'Ahmed Alghamdi', 'role': 'member'},
                {'name': 'Reema Alenezi', 'role': 'member'},
                {'name': 'Al-Anoud Alotaibi', 'role': 'member'},
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

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {success_count} members for {target_club_name}!'))