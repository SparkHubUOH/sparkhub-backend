from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .services.club_statistics import get_club_statistics
from .services.student_statistics import get_student_statistics
from .services.data_processor import preview_csv, summary_stats, groupby_agg, histogram
from .services.activity_statistics import get_activity_statistics
from .services.ml_prediction import train_activity_success_model, predict_activity_success

DEFAULT_CSV = "sample.csv"

class DataPreviewAPI(APIView):
    def get(self, request):
        name = request.query_params.get("file", DEFAULT_CSV)
        limit = int(request.query_params.get("limit", 50))
        try:
            rows = preview_csv(name, limit)
            return Response({"rows": rows})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SummaryStatsAPI(APIView):
    def get(self, request):
        name = request.query_params.get("file", DEFAULT_CSV)
        include = request.query_params.getlist("include") or None
        try:
            stats = summary_stats(name, include)
            return Response({"stats": stats})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GroupByAggAPI(APIView):
    def get(self, request):
        name = request.query_params.get("file", DEFAULT_CSV)
        by = request.query_params.get("by")
        agg_col = request.query_params.get("agg_col", by)
        agg_fn = request.query_params.get("agg_fn", "count")
        if not by:
            return Response({"error": "Parameter 'by' is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = groupby_agg(name, by, agg_col, agg_fn)
            return Response({"data": data, "by": by, "agg_col": agg_col, "agg_fn": agg_fn})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class HistogramAPI(APIView):
    def get(self, request):
        name = request.query_params.get("file", DEFAULT_CSV)
        col = request.query_params.get("col")
        bins = int(request.query_params.get("bins", 10))
        if not col:
            return Response({"error": "Parameter 'col' is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = histogram(name, col, bins)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ClubStatisticsAPI(APIView):
    def get(self, request):
        try:
            data = get_club_statistics()
            return Response(data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class StudentStatisticsAPI(APIView):
    def get(self, request):
        try:
            data = get_student_statistics()
            return Response(data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
class ActivityStatisticsView(APIView):

    def get(self, request):

        return Response(
            get_activity_statistics()
        )
        
@api_view(['GET'])
def train_ai_model(request):

    results = train_activity_success_model()

    return Response(results)

@api_view(['POST'])
def predict_activity(request):

    result = predict_activity_success(
        request.data
    )

    return Response(result)