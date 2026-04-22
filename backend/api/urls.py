from django.urls import path
from .views import test_api, predict_api, news_api


urlpatterns = [
    path("test/", test_api),
    path("predict/", predict_api),
    path("news/", news_api),
]