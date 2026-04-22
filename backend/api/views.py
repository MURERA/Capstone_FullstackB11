import sys
import os

from django.http import JsonResponse

# Tambahkan root project ke path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(BASE_DIR)

from ml.predict import predict_text


def test_api(request):
    return JsonResponse({"message": "API jalan!"})


def home(request):
    return JsonResponse({"message": "Welcome to Mental Health API"})


def predict_api(request):
    text = request.GET.get("text", "")

    if not text:
        return JsonResponse({"error": "Text is required"}, status=400)

    result = predict_text(text)

    return JsonResponse(result)

# berita
import requests

API_KEY = "39d231466a7e47e292281df70fbf7865"

def get_mental_health_news():
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": "mental health OR stress OR anxiety",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    articles = []

    for article in data.get("articles", [])[:5]:
        articles.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "image": article["urlToImage"]
        })

    return articles

def news_api(request):
    articles = get_mental_health_news()
    return JsonResponse({"articles": articles})