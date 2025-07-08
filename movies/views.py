from django.db.models import Avg
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models      import Movie, Review
from .serializers import MovieSerializer, ReviewSerializer
from .recommend import get_recommendations_after_last_watch

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list/retrieve movies with avg rating and nested reviews.
    """
    queryset         = Movie.objects.annotate(average_rating=Avg("reviews__rating"))
    serializer_class = MovieSerializer
    lookup_field     = "imdb_id"

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def review(self, request, imdb_id=None):
        """
        POST /api/movies/{imdb_id}/review/
        Body: { "rating": 4.5, "text": "Great movie!" }
        """
        movie = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewViewSet(viewsets.ModelViewSet):
    """
    (Optional) Direct CRUD on reviews if you need it.
    """
    queryset         = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommendations(request):
    """
        GET /api/recommendations/
        Returns a JSON array of movie titles recommended by Gemini.
        """
    recs = get_recommendations_after_last_watch(request.user, n=3)
    return Response({"recommendations": recs})
