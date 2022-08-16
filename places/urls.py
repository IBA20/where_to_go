from django.urls import path

from .views import PlaceView

urlpatterns = [
    path('<int:pk>/', PlaceView.as_view(), name='place_url'),
]
