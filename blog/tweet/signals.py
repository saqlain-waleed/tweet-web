from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Tweet

@receiver(post_delete, sender=Tweet)
def delete_tweet_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)  # Delete the file from storage
