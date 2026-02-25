from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('meuapp.urls')),
    path('api/acesso/', include('meuapp.urlsapi')),
    path('api/usuarios/', include('api.urlsapi')),
    path('accounts/', include('allauth.urls')),
]
