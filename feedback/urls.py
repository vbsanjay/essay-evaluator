from django.urls import path
from . import views

urlpatterns = [
    path("create_feedback/<uuid:essay_id>/", views.create_feedback, name="create_feedback"),
]