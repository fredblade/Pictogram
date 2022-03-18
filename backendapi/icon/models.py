from django.db import models
from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField, PPOIField
# Create your models here.
class IconItem(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='iconitem', related_query_name='iconitem')
    image = VersatileImageField(
        'Icon',
        upload_to='icons/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

class IconImage(models.Model):
    name = models.CharField(max_length=255)
    image = VersatileImageField(
        'Icon',
        upload_to='icons/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return self.name