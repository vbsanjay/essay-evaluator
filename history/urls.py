from django.urls import path
from . import views

urlpatterns = [
    path('history', views.history, name='history'),
    path('history/<uuid:essay_id>', views.detailed_report, name='detailed-report')
]