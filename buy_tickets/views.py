from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category,AirTicket,Airline,Comment,Rating,Like
from .serializer import CategorySerializer,AirTicketSerializer,AirLineSerializer,CommentCreateSerializer,RatingSerializer
from rest_framework import viewsets, views
from rest_framework.decorators import action
from .permissions import IsOwnerPermission, IsAdminOrActivePermission
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import filters






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
        passenger = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(passenger=passenger,post=user)
            like.delete()
            message = 'disliked'
        except Like.DoesNotExist:
            like = Like.objects.create(passenger=passenger,post=user,is_liked =True)
            like.save()
            message='liked'
        return Response(message, status=201)




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
    


