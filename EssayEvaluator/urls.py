from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", include("essays.urls")),
    path('feedbacks/', include('feedback.urls')),
    path('histories/', include('history.urls')),
    path("profiles/", include('profiles.urls'))
]
