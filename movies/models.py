from django.conf import settings
from django.db import models

class Movie(models.Model):
    imdb_id    = models.CharField(max_length=20, primary_key=True)
    title      = models.CharField(max_length=255)
    year       = models.PositiveSmallIntegerField()
    poster_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year})"

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