from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import requests

import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from .models import History
from ml.predict import predict_multiple 


class HomeView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to Mental Health API"})


class PredictMultiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        answers = request.data.get("answers")

        if not answers or not isinstance(answers, list):
            return Response({"error": "answers harus berupa list"}, status=400)

        #  PAKAI HYBRID ENGINE
        result = predict_multiple(answers)

        #  SIMPAN KE DATABASE
        History.objects.create(
            user=request.user,
            answers=answers,
            total_score=result.get("total_score"),
            category=result.get("category"),
            result_detail=result.get("details")
        )

        return Response(result)


class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = History.objects.filter(user=request.user).order_by('-created_at')

        result = []
        for item in data:
            result.append({
                "answers": item.answers,
                "score": item.total_score,
                "category": item.category,
                "created_at": item.created_at
            })

        return Response(result)


class NewsView(APIView):
    def get(self, request):
        category = request.GET.get("category", "").lower()

        # 🔥 mapping kategori → query yang lebih spesifik
        if category == "minimal":
            query = "mental wellness tips OR self care habits"
        elif category == "mild":
            query = "stress management tips OR relaxation techniques"
        elif category == "moderate":
            query = "anxiety coping strategies OR mental health help"
        elif category == "severe":
            query = "depression help therapy support mental health recovery"
        else:
            query = "mental health tips"

        url = "https://newsapi.org/v2/everything"

        params = {
            "q": query,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 10,
            "apiKey": settings.NEWS_API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        # 🔥 FILTER biar tidak random / politik / noise
        keywords = [
            "tips", "how", "guide", "therapy", "coping",
            "help", "mental", "health", "stress", "anxiety"
        ]

        filtered_articles = []

        for article in data.get("articles", []):
            title = (article.get("title") or "").lower()
            desc = (article.get("description") or "").lower()

            content = title + " " + desc

            # 🔥 hanya ambil artikel yang relevan
            if any(k in content for k in keywords):
                # skip artikel yang terlalu "news" atau politik
                if any(bad in content for bad in ["trump", "court", "law", "government"]):
                    continue

                filtered_articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "image": article.get("urlToImage")
                })

        # 🔥 fallback kalau hasil kosong
        if len(filtered_articles) == 0:
            for article in data.get("articles", [])[:5]:
                filtered_articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "image": article.get("urlToImage")
                })

        return Response({
            "articles": filtered_articles[:5]
        })