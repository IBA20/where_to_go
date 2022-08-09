from django.urls import path

from .views import BlankPageView, PlaceView

urlpatterns = [
    path('', BlankPageView.as_view()),
    path('<int:pk>', PlaceView.as_view()),
]
