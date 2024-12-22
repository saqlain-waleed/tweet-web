from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=250, null=False, blank=False)
    image = models.ImageField(upload_to='photos/', blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user)
    

class Search(models.Model):
    # Store the search text
    query = models.CharField(max_length=255, blank=False, null=False)

    # Store the timestamp when the search was created
    timestamp = models.DateTimeField(auto_now_add=True)

    # A field to store the user who performed the search (optional, can be linked to a user model)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.query)
