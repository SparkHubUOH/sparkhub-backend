from users.models import User
from clubs.models import Member
from django.db.models import Count, Q, F, FloatField
from django.db.models.functions import Cast


def get_student_statistics():

    students = (
        User.objects.filter(role='student')
        .annotate(

            clubs_joined=Count(
                'memberships',
                filter=Q(memberships__status='accepted'),
                distinct=True
            ),

            activities_attended=Count(
                'attended_activities',
                distinct=True
            ),
        )
    )

    data = []

    for student in students:

        engagement_score = (
            (student.activities_attended * 5)
            + (student.clubs_joined * 10)
            + (student.points / 10)
        )

        data.append({
            "student_id": student.id,

            "name": f"{student.first_name} {student.last_name}",

            "university_id": student.university_id,

            "clubs_joined": student.clubs_joined,

            "activities_attended": student.activities_attended,

            "points": student.points,

            "engagement_score": round(engagement_score, 2),
        })

    data = sorted(
        data,
        key=lambda x: x["engagement_score"],
        reverse=True
    )

    return {
        "students": data[:10],

        "total_students": len(data),

        "most_active_student": data[0] if data else None,

        "highest_points_student": (
            max(data, key=lambda x: x["points"])
            if data else None
        ),

        "top_students": data[:5],
    }