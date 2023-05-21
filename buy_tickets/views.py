from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category,AirTicket,Airline,Comment,Rating,Like,Favorite
from .serializer import CategorySerializer,AirTicketSerializer,AirLineSerializer,CommentCreateSerializer,RatingSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from .permissions import IsOwnerPermission, IsAdminOrActivePermission
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import filters
from django.core import files

from PIL import Image


import logging


logger = logging.getLogger(__name__)




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AirTicketViewSet(viewsets.ModelViewSet):
    queryset = AirTicket.objects.all()
    serializer_class = AirTicketSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'airline']
    search_fields = ['departure_city','arrival_city'] 
    ordering_fields = [ 'departure_date','departure_city']



class AirLinesViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirLineSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
    @action(methods=['POST', 'PATCH'], detail=True)
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['airline'] = pk
        rating = Rating.objects.filter(airline=pk, passenger=request.user).first()
        serializer = RatingSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response('Вы уже оставяли рейтинг,используйте PATCH запрос')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data,status=201)
            elif rating and request.method == 'PATCH':
                serializer.update(rating, serializer.validated_data)
                return Response ('updated',status=204)
    
    @action(methods=['POST'], detail=True)
    def like(self, request, pk=None):
        airline = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(passenger=user, airline=airline)
            like.delete()
            message = 'disliked'
        except Like.DoesNotExist:
            like = Like.objects.create(passenger=user, airline=airline, is_liked =True)
            like.save()
            message='liked'
        return Response(message, status=201)
    
    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk=None):
        airline = self.get_object()
        user = request.user
        try:
            favorite = Favorite.objects.get(passenger=user, airline=airline)
            favorite.delete()
            message = 'disfavorited'
        except Favorite.DoesNotExist:
            favorite = Favorite.objects.create(passenger=user, airline=airline, is_favorited =True)
            favorite.save()
            message='favorited'
        return Response(message, status=201)
    
    @action(['POST'], detail=True)
    def process_image(self, request, pk=None):
        airline = self.get_object()

        image_file = request.FILES.get('image')
        if not image_file:
            return Response('No image provided. Image processing skipped.', status=200)

        # Открыть изображение с помощью Pillow
        try:
            image = Image.open(image_file)
        except Exception as e:
            logger.exception('An error occured')
            return Response(str(e), status=400)
        return Response('Image processed and saved', status=200)   

    




class CommentView(viewsets.ModelViewSet):
    queryset  = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


