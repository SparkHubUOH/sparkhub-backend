import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from clubs.models import Activity 

User = get_user_model()

class Command(BaseCommand):
    help = 'Injects random participants into activities for model testing'

    def handle(self, *args, **options):
        all_student_ids = [i for i in range(169, 345) if i != 203]
        
        activities = Activity.objects.all()
        
        if not activities.exists():
            self.stdout.write(self.style.ERROR('No activities found in the database!'))
            return

        total_injected = 0

        for activity in activities:
            min_random = int(activity.max_attendees * 0.4)
            max_random = activity.max_attendees
            num_to_add = random.randint(min_random, max_random)
            
            selected_students = random.sample(all_student_ids, min(num_to_add, len(all_student_ids)))

            for student_id in selected_students:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        IF NOT EXISTS (SELECT 1 FROM clubs_activity_participants 
                                     WHERE activity_id = %s AND user_id = %s)
                        BEGIN
                            INSERT INTO clubs_activity_participants (activity_id, user_id)
                            VALUES (%s, %s)
                        END
                    """, [activity.id, student_id, activity.id, student_id])
                
            total_injected += len(selected_students)
            self.stdout.write(f"Activity '{activity.title_ar}': Added {len(selected_students)} participants.")

        self.stdout.write(self.style.SUCCESS(f'Successfully injected {total_injected} participation records!'))