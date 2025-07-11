# Generated by Django 5.2.4 on 2025-07-08 15:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.AutoField(primary_key=True, serialize=False)),
                ('Title', models.TextField(blank=True, null=True)),
                ('IMDb_Rating', models.FloatField(blank=True, null=True)),
                ('Year', models.BigIntegerField(blank=True, null=True)),
                ('Certificates', models.TextField(blank=True, null=True)),
                ('Genre', models.TextField(blank=True, null=True)),
                ('Director', models.TextField(blank=True, null=True)),
                ('Star_Cast', models.TextField(blank=True, null=True)),
                ('MetaScore', models.FloatField(blank=True, null=True)),
                ('Poster_src', models.TextField(blank=True, null=True)),
                ('Duration_minutes', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('watchlist', models.TextField(blank=True, null=True)),
                ('friendlist', models.TextField(blank=True, null=True)),
                ('liked', models.TextField(blank=True, null=True)),
                ('disliked', models.TextField(blank=True, null=True)),
                ('favorite_genre', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlists', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('text', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('user', 'movie')},
            },
        ),
        migrations.CreateModel(
            name='WatchlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('watchlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='movies.watchlist')),
            ],
            options={
                'unique_together': {('watchlist', 'movie')},
            },
        ),
    ]
