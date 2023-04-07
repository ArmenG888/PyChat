from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime
User = settings.AUTH_USER_MODEL
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_online = models.DateTimeField(default=timezone.now)
    def online(self):
        widthin_last_seconds = timezone.now() - datetime.timedelta(minutes=5)
        if self.last_online > widthin_last_seconds:
            return "🟢"
        else:
            return "🔴"