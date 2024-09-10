from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", include("essays.urls")),
    path('feedbacks/', include('feedback.urls')),
    path('histories/', include('history.urls')),
    path("profiles/", include('profiles.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)