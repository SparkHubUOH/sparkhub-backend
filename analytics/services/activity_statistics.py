from clubs.models import Activity
import pandas as pd


def get_activity_statistics():

    activities = Activity.objects.select_related('club').prefetch_related('participants')

    data = []

    for activity in activities:

        participants_count = activity.participants.count()

        max_attendees = activity.max_attendees or 0

        attendance_rate = (
            (participants_count / max_attendees) * 100
            if max_attendees > 0 else 0
        )

        data.append({
            "activity_id": activity.id,
            "title": activity.title,
            "club_name": activity.club.club_name,
            "participants_count": participants_count,
            "location": activity.location,
            "date": activity.date,

            "max_attendees": max_attendees,

            "attendance_rate": round(attendance_rate, 2),

            "performance_status": (
                "Excellent"
                if attendance_rate >= 80 else
                "Good"
                if attendance_rate >= 50 else
                "Weak"
            ),
        })

    df = pd.DataFrame(data)

    if df.empty:
        return {
            "activities": [],
            "total_activities": 0,
        }

    return {

        "activities": (
            df.sort_values(
                by="participants_count",
                ascending=False
            )
            .head(10)
            .to_dict(orient="records")
        ),

        "total_activities": len(df),

        "most_popular_activity": (
            df.sort_values(
                by="participants_count",
                ascending=False
            )
            .head(1)
            .to_dict(orient="records")
        ),

        "highest_attendance_activity": (
            df.sort_values(
                by="attendance_rate",
                ascending=False
            )
            .head(1)
            .to_dict(orient="records")
        ),

        "top_activities": (
            df.sort_values(
                by="participants_count",
                ascending=False
            )
            .head(5)
            .to_dict(orient="records")
        ),
    }