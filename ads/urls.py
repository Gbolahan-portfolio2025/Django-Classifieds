from django.urls import path
from . import views

urlpatterns = [
    path("", views.ad_list, name="ad_list"),
    path("ads/<slug:slug>/", views.ad_detail, name="ad_detail"),
    path("ads/create/", views.ad_create, name="ad_create"),
    path("ads/<slug:slug>/edit/", views.ad_update, name="ad_update"),
    path("ads/<slug:slug>/delete/", views.ad_delete, name="ad_delete"),
    path("ads/my-ads/", views.my_ads, name="my_ads"),
]
