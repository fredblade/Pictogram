from django.contrib import admin
from .models import PostItem, CommentItem

admin.site.register(PostItem)
admin.site.register(CommentItem)