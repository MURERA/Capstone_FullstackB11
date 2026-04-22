from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = []
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]