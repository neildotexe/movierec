# load_movies.py

import os
import sys
import django
import pandas as pd

csv_path = os.path.join(os.path.dirname(__file__), "IMDb_Dataset_2.csv")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ---------- Setup Django Environment ----------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movierec.settings')  # Replace with your actual project name
django.setup()

from movies.models import Movie  # Replace with your actual app name

# ---------- Read and Clean Dataset ----------
df = pd.read_csv(csv_path)

# Filter data from 2020 onward
df = df[df['Year'] >= 2020]

# Rename columns to match Django model field names
df.rename(columns={
    "IMDb Rating": "IMDb_Rating",
    "Star Cast": "Star_Cast",
    "Poster-src": "Poster_src",
    "Duration (minutes)": "Duration_minutes"
}, inplace=True)

# ---------- Insert into Django DB ----------
movies = []
for _, row in df.iterrows():
    movie = Movie(
        Title=row.get('Title'),
        IMDb_Rating=row.get('IMDb_Rating'),
        Year=row.get('Year'),
        Certificates=row.get('Certificates'),
        Genre=row.get('Genre'),
        Director=row.get('Director'),
        Star_Cast=row.get('Star_Cast'),
        MetaScore=row.get('MetaScore'),
        Poster_src=row.get('Poster_src'),
        Duration_minutes=row.get('Duration_minutes')
    )
    movies.append(movie)

# Bulk insert all movie records
Movie.objects.bulk_create(movies)
print(f"{len(movies)} movies saved to the database.")
