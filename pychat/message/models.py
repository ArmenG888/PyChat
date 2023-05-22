from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class dm(models.Model):
    name = models.CharField(max_length=50, default="")
    list_of_people = models.ManyToManyField(User)
    gpt = models.BooleanField(default=False)

    def __str__(self):
        return self.name
class message(models.Model):
    text = models.TextField(default="")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(dm, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    reply = models.ForeignKey("message.message", blank=True,null=True,default="", on_delete=models.CASCADE)
