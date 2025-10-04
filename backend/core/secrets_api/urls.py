from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include('docs.urls')),
    path('api/', include('tickets.urls')),
    path('api/', include('users.urls')),
]

urlpatterns += staticfiles_urlpatterns()
