
from django.urls import path
from .views import generate_image, generate_captions

urlpatterns = [
    path("api/generate/", generate_image, name="generate_image"),
    path("api/generate-captions/", generate_captions),
]
