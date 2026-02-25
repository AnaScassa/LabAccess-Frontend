from django.urls import include, path
from rest_framework import routers
from meuapp.api import UserViewSet
from api.apiview import UserViewSetApi

router = routers.DefaultRouter()
router.register(r"userAuth", UserViewSetApi) 

urlpatterns = [
    path('', include(router.urls)),
    path("userAuth2/", UserViewSetApi.as_view({'get': 'list'})),
]