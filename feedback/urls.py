from django.urls import path
from . import views

urlpatterns = [
    path('feedback/<uuid:feedback_id>/', views.feedback, name='feedback'),
    path("create_feedback/<uuid:essay_id>/", views.create_feedback, name="create_feedback"),   
]