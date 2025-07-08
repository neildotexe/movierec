
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from movies.views import MovieViewSet, ReviewViewSet, recommendations, my_reviews, WatchlistViewSet
from movies.views import * 



router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"watchlists",WatchlistViewSet, basename="watchlist")


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', filter_movies, name='home'),
    path("api/", include(router.urls)),
    path("api/api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("api/recommendations/", recommendations, name="recommendations"),
    path("api/my-reviews/", my_reviews, name="my-reviews")
]
