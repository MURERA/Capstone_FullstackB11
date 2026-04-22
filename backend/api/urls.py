from django.urls import path
from .views import HomeView, PredictMultiView, HistoryView, NewsView


urlpatterns = [
    path('', HomeView.as_view()),
    path('predict-multi/', PredictMultiView.as_view()),
    path('history/', HistoryView.as_view()),
    path('news/', NewsView.as_view()),
]