from django.urls import path

from .views import FavThingView, FavThingDetail


app_name = "favthing"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('favorite-things/', FavThingView.as_view()),
    path('favorite-things/<pk>', FavThingDetail.as_view()),
]
