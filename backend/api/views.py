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
from ml.predict import predict_text


class HomeView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to Mental Health API"})


class PredictMultiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        answers = request.data.get("answers")

        if not answers or not isinstance(answers, list):
            return Response({"error": "answers harus berupa list"}, status=400)

        total_score = 0
        detail_results = []

        for text in answers:
            result = predict_text(text)

            negative = result.get("negative", 0)
            neutral = result.get("neutral", 0)

            if negative > 0.6:
                score = 2
            elif neutral > 0.5:
                score = 1
            else:
                score = 0

            total_score += score
            detail_results.append(result)

        if total_score <= 3:
            category = "Normal"
        elif total_score <= 6:
            category = "Mild"
        elif total_score <= 10:
            category = "Moderate"
        else:
            category = "Severe"

        History.objects.create(
            user=request.user,
            answers=answers,
            total_score=total_score,
            category=category,
            result_detail=detail_results
        )

        return Response({
            "total_score": total_score,
            "category": category,
            "detail": detail_results
        })


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
        url = "https://newsapi.org/v2/everything"

        params = {
            "q": "mental health OR stress OR anxiety",
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": settings.NEWS_API_KEY
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

        return Response({"articles": articles})