from django.urls import path
from .views import DataPreviewView, ProphetPredictView

urlpatterns = [
    path('analytics/data-preview/', DataPreviewView.as_view(), name='data-preview'),
    path('analytics/predict/', ProphetPredictView.as_view(), name='prophet-predict'),
]
