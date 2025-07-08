from django.conf import settings
from django.db import models

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    Title = models.TextField(null=True, blank=True)
    IMDb_Rating = models.FloatField(null=True, blank=True)
    Year = models.BigIntegerField(null=True, blank=True)
    Certificates = models.TextField(null=True, blank=True)
    Genre = models.TextField(null=True, blank=True)
    Director = models.TextField(null=True, blank=True)
    Star_Cast = models.TextField(null=True, blank=True)
    MetaScore = models.FloatField(null=True, blank=True)
    Poster_src = models.TextField(null=True, blank=True)
    Duration_minutes = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.Title or f"Movie {self.movie_id}"
    
class User(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    watchlist = models.TextField(null=True, blank=True)
    friendlist = models.TextField(null=True, blank=True)
    liked = models.TextField(null=True, blank=True)
    disliked = models.TextField(null=True, blank=True)
    favorite_genre = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
    
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    rating = models.DecimalField(max_digits=2, decimal_places=1)  #0.0 to 9.9
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} -> {self.movie.title}: {self.rating}"
    

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlists")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class WatchlistItem(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name="items")
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("watchlist", "movie")

    def __str__(self):
        return f"{self.movie.title} in {self.watchlist.name}"
