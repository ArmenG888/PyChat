from django.db import models
from django.contrib.auth.models import User


class dm(models.Model):
    name = models.CharField(max_length=50, default="")
    list_of_people = models.ManyToManyField(User)

    def __str__(self):
        return self.name
class message(models.Model):
    text = models.TextField(default="")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(dm, on_delete=models.CASCADE)
    

