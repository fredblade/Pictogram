from rest_flex_fields import FlexFieldsModelSerializer
from .models import PostItem, CommentItem, ImageItem
from django.contrib.auth.models import User
from versatileimagefield.serializers import VersatileImageFieldSerializer
import base64, uuid
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid
        
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            
            try:
                decoded_file = base64.b64decode(data)
                # decoded_file = base64.urlsafe_b64decode(data)
                # missing_padding = len(decoded_file) % 4
                # if missing_padding:
                # decoded_file += b'=' * (4 - missing_padding)
                # print(decoded_file)
            except TypeError:
                self.fail('invalid_image')
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension,)
            data = ContentFile(decoded_file, name=complete_file_name)
        return super(Base64ImageField, self).to_internal_value(data)
    
    def get_file_extension(self, file_name, decoded_file):
        import imghdr
        
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        
        return extension


class PostItemSerializer(FlexFieldsModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    
    # username = serializers.CharField(max_length=255)
    # image = VersatileImageFieldSerializer(
    #     sizes=[
    #         ('full_size', 'url'),
    #         ('thumbnail', 'thumbnail__100x100'),
    #     ]
    # )
    class Meta:
        model = PostItem
        fields = ['pk', 'content', 'created', 'updated', 'user_id', 'image']


class PostItemListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField(max_length=255)
    image = serializers.CharField(max_length=255)
    updated = serializers.DateField()
    created = serializers.DateField()
    user_id = serializers.ModelField(model_field=PostItem()._meta.get_field('user_id'))
    # user_id = serializers.ModelField(model_field=CommentItem()._meta.get_field('user_id'))
    # image_ppoi = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UsernameField(serializers.RelatedField):
    def to_representation(self, value):
        print('test', value)
        username = value.username
        return username


class CommentItemSerializer(FlexFieldsModelSerializer):
    # username = UsernameField(many=False, read_only=True)
    # username = serializers.SlugRelatedField(
    #     many=False,
    #     read_only=True,
    #     slug_field='usernamo'
    # )
    class Meta:
        model = CommentItem
        fields = ['pk', 'title', 'created', 'updated', 'user_id', 'post_id']
        expandable_fields = {
            'post_id': 'posts.CategorySerializer',
            'user_id': 'posts.UserSerializer',
            # 'username': 'posts.UserSerializer',
        }


class CommentItemListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    post_id = serializers.ModelField(model_field=CommentItem()._meta.get_field('post_id'))
    user_id = serializers.ModelField(model_field=CommentItem()._meta.get_field('user_id'))
    username = serializers.CharField(max_length=255)
    created = serializers.DateField()
    
    # class Meta:
    #     model = CommentItem
    #     fields = ['pk', 'title', 'created', 'post_id', 'user_id']
    # class Meta:
    #     model = User
    #     fields = ['user_id', 'username']


class ImageItemSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes='product_headshot'
    )
    
    class Meta:
        model = ImageItem
        fields = ['pk', 'name', 'image']
