from rest_framework import serializers
from .models import Movie, Review, Watchlist, WatchlistItem

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id","user","rating","text","created_at"]



class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)  # Computed from related reviews
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            "movie_id",
            "Title",
            "IMDb_Rating",
            "Year",
            "Certificates",
            "Genre",
            "Director",
            "Star_Cast",
            "MetaScore",
            "Poster_src",
            "Duration_minutes",
            "average_rating",
            "reviews"
        ]

class WatchlistItemSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField(read_only=True)
    

    class Meta:
        model = WatchlistItem
        fields = ["id", "movie", "added_at"]

class WatchlistSerializer(serializers.ModelSerializer):
    items = WatchlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Watchlist
        fields = ["id", "name", "created_at", "items"]