from django.conf import settings
from django.db import models


class Note(models.Model):
    text = models.CharField(max_length=300, blank=False, null=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}, created by {self.user}"
