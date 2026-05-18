from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import os

class DataPreviewView(APIView):
    """
    عرض عينة من بيانات تحليلية باستخدام Pandas
    """

    def get(self, request):
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'sample.csv')
        df = pd.read_csv(csv_path)
        preview = df.head(10).to_dict(orient='records')
        return Response(preview)


class ProphetPredictView(APIView):
    """
    التنبؤ باستخدام Prophet
    """

    def get(self, request):
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'time_series.csv')
        df = pd.read_csv(csv_path)
        df.columns = ['ds', 'y']

        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)

        result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(10).to_dict(orient='records')
        return Response(result)
