from django.urls import path
from .views import ActivityStatisticsView, ClubStatisticsAPI, DataPreviewAPI, SummaryStatsAPI, GroupByAggAPI, HistogramAPI, StudentStatisticsAPI, predict_activity, train_ai_model

urlpatterns = [
    path('data/preview/', DataPreviewAPI.as_view()),
    path('data/summary/', SummaryStatsAPI.as_view()),
    path('data/groupby/', GroupByAggAPI.as_view()),
    path('data/histogram/', HistogramAPI.as_view()),
    path('clubs/statistics/', ClubStatisticsAPI.as_view()),
    path('students/statistics/', StudentStatisticsAPI.as_view()),
    path('activities/statistics/', ActivityStatisticsView.as_view()),
    path('train-model/',train_ai_model),
    path('predict-activity/',predict_activity),
]
