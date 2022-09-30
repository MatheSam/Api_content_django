from django.urls import path
from . import views

urlpatterns = [
    path("contents/", views.ContentsView.as_view()),
    path("contents/<int:content_id>/", views.ContentDetailView.as_view()),
    path("contents/filter/", views.ContentFindView.as_view()),
]
