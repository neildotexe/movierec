from django.db.models import Avg
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models      import Movie, Review, Watchlist, WatchlistItem
from .serializers import MovieSerializer, ReviewSerializer, WatchlistSerializer
from .recommend import get_recommendations_after_last_watch

from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def filter_movies(request):
    movies = Movie.objects.all() 
    if request.method == "POST":
        print("hellloooo")
        rating = request.POST.get("imdb_rating")
        year_range = request.POST.get("year_range")
        genre = request.POST.get("genre")
        certificate = request.POST.get("certificate")
        sort_by = request.POST.get("sort_by")

        movies = Movie.objects.all()

        if rating:
            movies = movies.filter(IMDb_Rating__gte=float(rating))

        if year_range:
            start = int(year_range)
            movies = movies.filter(Year__gte=start, Year__lt=start+10)

        if genre:
            movies = movies.filter(Genre__icontains=genre)

        if certificate:
            movies = movies.filter(Certificates__icontains=certificate)

        if sort_by == "rating_desc":
            movies = movies.order_by("-IMDb_Rating")
        elif sort_by == "rating_asc":
            movies = movies.order_by("IMDb_Rating")
        elif sort_by == "year_desc":
            movies = movies.order_by("-Year")
        elif sort_by == "year_asc":
            movies = movies.order_by("Year")

    return render(request, "index.html", {"movies": movies})


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list/retrieve movies with avg rating and nested reviews.
    """
    queryset         = Movie.objects.annotate(average_rating=Avg("reviews__rating"))
    serializer_class = MovieSerializer
    lookup_field     = "imdb_id"
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_reviews(request):
    """
    GET /api/my-reviews/
    Returns only the reviews created by the authenticated user.
    """
    qs = Review.objects.filter(user=request.user)
    serializer = ReviewSerializer(qs, many=True)
    return Response(serializer.data)

class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class   = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def add_movie(self, request, pk=None):
        wl = self.get_object()
        title = request.data.get("movie_title")
        if not title:
            return Response({"detail":"movie_title is required"}, status=status.HTTP_400_BAD_REQUEST)

        # lookup by title (case‐insensitive)
        try:
            movie = Movie.objects.get(title__iexact=title)
        except Movie.DoesNotExist:
            return Response({"detail":f"No movie found with title '{title}'"}, status=status.HTTP_404_NOT_FOUND)

        item, created = WatchlistItem.objects.get_or_create(watchlist=wl, movie=movie)
        return Response(
            {"added": created, "movie": movie.title},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["post"])
    def remove_movie(self, request, pk=None):
        wl = self.get_object()
        title = request.data.get("movie_title")
        if not title:
            return Response({"detail":"movie_title is required"}, status=status.HTTP_400_BAD_REQUEST)

        # lookup the item by title
        item = WatchlistItem.objects.filter(
            watchlist=wl,
            movie_title_iexact=title
        ).first()

        if not item:
            return Response({"removed": False, "detail":f"No '{title}' in this watchlist"}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response({"removed": True, "movie": title})