from .serializers import PostItemSerializer, ImageItemSerializer, CommentItemSerializer, CommentItemListSerializer, \
    PostItemListSerializer
from .models import PostItem, ImageItem, CommentItem
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet
from rest_flex_fields import is_expanded
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
import os


# Create your views here.

# class PostItemViewSet(FlexFieldsMixin, ModelViewSet):
#     serializer_class = PostItemSerializer
#     permit_list_expands = ['category']
#     filterset_fields = ('user',)
#
#     def get_queryset(self):
#         queryset = PostItem.objects.all()
#
#         if is_expanded(self.request, 'user'):
#             queryset = queryset.prefetch_related('user')
#
#         return queryset
class PostItemViewSet(FlexFieldsMixin, APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        print(request.user.username)
        print(request.user.id)
        # postitems = PostItem.objects.filter(user=request.user.id)
        # postitems = PostItem.objects.all()
        postitems = PostItem.objects.raw(r'select posts_postitem.*, auth_user.username from posts_postitem left JOIN '
                                         r'auth_user on posts_postitem.user_id_id = auth_user.id')
        serializer = PostItemListSerializer(postitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        print("user", request.user.id)
        data = {
            'content': request.data.get('content'),
            'user_id': request.user.id,
            'username': request.user.username,
            'image': request.data.get('image')
        }
        serializer = PostItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostItemDetailApiView(FlexFieldsMixin, APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, post_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return PostItem.objects.get(id=post_id)
        except PostItem.DoesNotExist:
            return None
    
    # 3. Retrieve
    def get(self, request, post_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        print('getting post', post_id)
        item = PostItem.objects.raw(r'select posts_postitem.*, auth_user.username from posts_postitem left JOIN '
                                    r'auth_user on posts_postitem.user_id_id = auth_user.id where posts_postitem.id = '
                                    fr'{post_id}')
        print(item)
        try:
            item = item[0]
        except:
            Response({'Error, not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostItemListSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 4. Update
    def put(self, request, post_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(post_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with post_id does not exists or not yours"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'content': request.data.get('content'),
            'user_id': request.user.id
        }
        serializer = PostItemSerializer(instance=todo_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 5. Delete
    def delete(self, request, post_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        # todo_instance = self.get_object(post_id, request.user.id)
        todo_instance = PostItem.objects.filter(id=post_id, user_id=request.user.id).first()
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists or you are not the owner"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PostItemSerializer(todo_instance)
        imgPath = serializer.data.get('image')
        # print(f'{str(imgPath)}')
        # print(os.getcwd())
        # .. doesn't work to go back 1 directory
        if os.path.exists(f'{os.getcwd()}{str(imgPath)}'):
            os.remove(f'{os.getcwd()}{str(imgPath)}')
        else:
            print("The file does not exist")
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
        # print(serializer.data)
        # return Response(
        #     {"res": "temp res!"},
        #     status=status.HTTP_200_OK
        # )


class PostsUserApiView(FlexFieldsMixin, APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, user_id, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        print(user_id)
        # postitems = PostItem.objects.filter(user=request.user.id)
        postitems = PostItem.objects.filter(user_id=user_id)
        serializer = PostItemSerializer(postitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentItemViewSet(FlexFieldsMixin, APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    # 1. List all
    def get(self, request, post_id, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # postitems = PostItem.objects.filter(user=request.user.id)
        # comments = CommentItem.objects.filter(post_id=post_id)
        comments = CommentItem.objects.raw(r'select posts_commentitem.id, posts_commentitem.title, '
                                           'posts_commentitem.created, posts_commentitem.post_id_id, '
                                           'posts_commentitem.user_id_id, auth_user.username from '
                                           'posts_commentitem '
                                           'left JOIN auth_user on posts_commentitem.user_id_id = auth_user.id where '
                                           f'posts_commentitem.post_id_id = {post_id}')
        
        serializer = CommentItemListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(comments, status=status.HTTP_200_OK)
    
    # 2. Create
    def post(self, request, post_id, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        print("USER:", request.user.id)
        print(post_id)
        data = {
            'title': request.data.get('title'),
            'post_id': post_id,
            'user_id': request.user.id,
            
            # 'username': request.user.username,
        }
        serializer = CommentItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 5. Delete
    def delete(self, request, post_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        # Router uses post_id as parameter but comment_id is needed
        comment_id = post_id
        # instance = self.get_object(post_id, request.user.id)
        instance = CommentItem.objects.filter(id=comment_id, user_id=request.user.id)
        if not instance:
            return Response(
                {"res": "Comment does not exists or you are not the owner"},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
