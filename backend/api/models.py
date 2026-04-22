from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # input
    answers = models.JSONField()

    # hasil ML
    total_score = models.IntegerField()
    category = models.CharField(max_length=20)

    # optional detail
    result_detail = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.category}"