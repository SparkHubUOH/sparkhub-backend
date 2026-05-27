import pandas as pd
from clubs.models import Club


def get_club_statistics():
    clubs = Club.objects.filter(status='active')

    data = []

    for club in clubs:
        total_members = club.memberships.filter(
            status='accepted'
        ).count()

        total_activities = club.activities.count()

        total_participants = sum(
            activity.participants.count()
            for activity in club.activities.all()
        )

        avg_participants = (
            total_participants / total_activities
            if total_activities > 0 else 0
        )

        participation_rate = (
            (total_participants / total_members) * 100
            if total_members > 0 else 0
        )

        activity_frequency = (
            total_activities / total_members
            if total_members > 0 else 0
        )

        club_score = (
            (total_activities * 4)
            + (total_participants * 3)
            + (total_members * 2)
            + club.points
        )

        data.append({
            "club_id": club.id,
            "club_name": club.club_name,

            "members_count": total_members,
            "activities_count": total_activities,
            "participants_count": total_participants,

            "avg_participants": round(avg_participants, 2),

            "participation_rate": round(participation_rate, 2),

            "activity_frequency": round(activity_frequency, 2),

            "club_score": round(club_score, 2),

            "points": club.points,
            "status": club.status,
        })

    df = pd.DataFrame(data)

    if df.empty:
        return {
            "clubs": [],
            "total_clubs": 0,
            "most_active_club": [],
            "highest_engagement": [],
            "top_clubs": [],
            "inactive_clubs": [],
        }

    return {
        "clubs": df.to_dict(orient="records"),

        "total_clubs": len(df),

        "most_active_club": (
            df.sort_values(
                by="activities_count",
                ascending=False
            )
            .head(1)
            .to_dict(orient="records")
        ),

        "highest_engagement": (
            df.sort_values(
                by="participants_count",
                ascending=False
            )
            .head(1)
            .to_dict(orient="records")
        ),

        "top_clubs": (
            df.sort_values(
                by="club_score",
                ascending=False
            )
            .head(5)
            .to_dict(orient="records")
        ),

        "inactive_clubs": (
            df[
                (df["activities_count"] == 0)
                | (df["participants_count"] == 0)
            ]
            .to_dict(orient="records")
        ),
    }