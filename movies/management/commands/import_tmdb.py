# movies/management/commands/import_imdb.py  (you can rename it import_tmdb.py)

import os, time
import requests
from django.core.management.base import BaseCommand
from movies.models import Movie

API_KEY = os.environ["TMDB_API_KEY"]
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Discover movies from 2022–2024
DISCOVER_URL = (
    "https://api.themoviedb.org/3/discover/movie"
    f"?api_key={API_KEY}"
    "&primary_release_date.gte=2022-01-01"
    "&primary_release_date.lte=2024-12-31"
    "&sort_by=primary_release_date.desc"
    "&page={page}"
)

# Upcoming movies
UPCOMING_URL = (
    "https://api.themoviedb.org/3/movie/upcoming"
    f"?api_key={API_KEY}"
    "&region=IN"     # or your desired region
    "&page={page}"
)

class Command(BaseCommand):
    help = "Import recent (2022–2024) and upcoming movies via TMDb API"

    def fetch_page(self, url_template, max_pages=2):
        """Generator: yields movie dicts for up to max_pages pages."""
        for page in range(1, max_pages+1):
            url = url_template.format(page=page)
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json().get("results", [])
            if not data:
                break
            for m in data:
                yield m
            time.sleep(0.25)  # throttle

    def handle(self, *args, **options):
        # 1) Recent releases
        self.stdout.write("🔄 Importing recent releases from TMDb...")
        for m in self.fetch_page(DISCOVER_URL, max_pages=5):
            imdb_id = m.get("id")  # TMDb ID
            title   = m.get("title")
            date    = m.get("release_date", "")
            year    = int(date.split("-")[0]) if date else 0
            poster  = IMAGE_BASE + m.get("poster_path") if m.get("poster_path") else ""

            Movie.objects.update_or_create(
                imdb_id=str(imdb_id),
                defaults={"title": title, "year": year, "poster_url": poster}
            )
            self.stdout.write(f"  • {title} ({year})")

        # 2) Upcoming releases
        self.stdout.write("🔄 Importing upcoming releases from TMDb...")
        for m in self.fetch_page(UPCOMING_URL, max_pages=3):
            imdb_id = m.get("id")
            title   = m.get("title")
            date    = m.get("release_date", "")
            year    = int(date.split("-")[0]) if date else 0
            poster  = IMAGE_BASE + m.get("poster_path") if m.get("poster_path") else ""

            Movie.objects.update_or_create(
                imdb_id=str(imdb_id),
                defaults={"title": title, "year": year, "poster_url": poster}
            )
            self.stdout.write(f"  • {title} ({year or 'upcoming'})")

        self.stdout.write(self.style.SUCCESS("✅ import_tmdb complete!"))
