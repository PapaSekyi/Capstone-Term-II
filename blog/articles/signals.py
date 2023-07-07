import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import article

@receiver(pre_save, sender=article)
def add_slug(sender, instance, **kwargs):
    print('add_slug function called')
    if instance and not instance.slug:
        unique_id = uuid.uuid4().hex[:10].upper() # Generate a 10-character uppercase UUID
        slug = slugify(unique_id)
        instance.slug = slug