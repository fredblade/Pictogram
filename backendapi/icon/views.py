from .serializers import IconItemSerializer
from .models import IconItem, IconImage
from rest_framework.viewsets import ModelViewSet
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet
from rest_flex_fields import is_expanded
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


# Create your views here.
class ImageItemViewSet(FlexFieldsMixin, APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # print(request.user.username)
        # print(request.user.id)
        # postitems = PostItem.objects.filter(user=request.user.id)
        postitems = IconItem.objects.filter(user_id=request.user.id)
        serializer = IconItemSerializer(postitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        # print("ERROR", request.user.id)
        data = {
            'user_id': request.user.id,
            'image': request.data.get('image')
        }
        serializer = IconItemSerializer(data=data)
        if serializer.is_valid():
            instance = IconItem.objects.filter(user_id=request.user.id)
            instance.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IconUserApiView(FlexFieldsMixin, APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        print(user_id)
        # postitems = PostItem.objects.filter(user=request.user.id)
        iconitems = IconItem.objects.filter(user_id=user_id)
        serializer = IconItemSerializer(iconitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
