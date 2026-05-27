from clubs.models import Activity, Club
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

def prepare_activity_dataset():

    activities = Activity.objects.select_related('club').all()

    data = []

    for activity in activities:

        participants_count = activity.participants.count()

        max_attendees = activity.max_attendees or 1

        attendance_rate = round(
            (participants_count / max_attendees) * 100,
            2
        )

        club_activities_count = activity.club.activities.count()

        avg_club_attendance = 0

        club_activities = activity.club.activities.all()

        total_attendance = sum(
            a.participants.count()
            for a in club_activities
        )

        if club_activities.count() > 0:
            avg_club_attendance = (
                total_attendance / club_activities.count()
            )

        data.append({
            "activity_title": activity.title,

            "category": activity.category,

            "participants_count": participants_count,

            "max_attendees": max_attendees,

            "attendance_rate": attendance_rate,

            "club_activities_count": club_activities_count,

            "avg_club_attendance": round(
                avg_club_attendance,
                2
            ),
        })

    return pd.DataFrame(data)


def classify_success(rate):

    if rate >= 70:
        return "High"

    elif rate >= 40:
        return "Medium"

    return "Low"


def prepare_ml_data():

    df = prepare_activity_dataset()

    if df.empty:
        return None

    df["success_level"] = df["attendance_rate"].apply(
        classify_success
    )

    encoder = LabelEncoder()

    df["category_encoded"] = encoder.fit_transform(
        df["category"]
    )

    X = df[
        [
            "category_encoded",
            "max_attendees",
            "club_activities_count",
            "avg_club_attendance",
        ]
    ]

    y = df["success_level"]

    return X, y, encoder, df


def train_activity_success_model():

    result = prepare_ml_data()

    if result is None:
        return {
            "error": "No activity data available"
        }

    X, y, encoder, df = result

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    return {
        "accuracy": round(accuracy * 100, 2),

        "total_activities": len(df),

        "training_samples": len(X_train),

        "testing_samples": len(X_test),

        "features": list(X.columns),

        "success_distribution": (
            df["success_level"]
            .value_counts()
            .to_dict()
        )
    }
    
def predict_activity_success(data):

    result = prepare_ml_data()

    if result is None:
        return {
            "error": "No training data available"
        }

    X, y, encoder, df = result

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    category_encoded = encoder.transform(
        [data["category"]]
    )[0]

    input_data = np.array([[
        category_encoded,
        data["max_attendees"],
        data["club_activities_count"],
        data["avg_club_attendance"]
    ]])

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    confidence = round(
        max(probabilities) * 100,
        2
    )

    return {
        "prediction": prediction,
        "confidence": confidence
    }