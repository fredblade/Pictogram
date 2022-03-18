from django.db import models
from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField, PPOIField


class PostItem(models.Model):
    content = models.TextField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postitems', related_query_name='postitem')
    # username = models.CharField(max_length=255)
    image = VersatileImageField(
        'Image',
        upload_to='postimages/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']


class CommentItem(models.Model):
    title = models.CharField(max_length=255)
    post_id = models.ForeignKey(PostItem, on_delete=models.CASCADE, related_name='commentsitems',
                                related_query_name='commentitem', blank=True, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentsitems',
                                related_query_name='commentitem', blank=True, null=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class ImageItem(models.Model):
    name = models.CharField(max_length=255)
    image = VersatileImageField(
        'Image',
        upload_to='postimages/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return self.name
