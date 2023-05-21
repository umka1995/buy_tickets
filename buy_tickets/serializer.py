from rest_framework import serializers
from .models import Category, AirTicket, Airline, Rating,Comment
from django.contrib.auth import get_user_model
from django.db.models import Avg


User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class AirLineSerializer(serializers.ModelSerializer):
    passenger = serializers.ReadOnlyField(source='passenger.name')
    class Meta:
        model = Airline
        fields = ['title','passenger']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = instance.comments.count()
        representation['rating'] = RatingSerializer(Rating.objects.filter(airline=instance.pk), many=True).data
        representation['favorites'] = instance.favorites.count()
        representation['likes_count'] = instance.likes.count()
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']

        return representation




class AirTicketSerializer(serializers.ModelSerializer):
    passenger = serializers.ReadOnlyField(source='passenger.name')
    class Meta:
        model = AirTicket
        fields = '__all__'

    # def validate(self, data):
    #     departure_city = data.get('departure_city')
    #     arrival_city = data.get('arrival_city')
    #     departure_date = data.get('departure_date')
    #     if AirTicket.objects.filter(departure_city=departure_city, arrival_city=arrival_city, departure_date=departure_date):
    #         raise serializers.ValidationError(
    #             'билет с указанными параметрами уже сущесвует '
    #         )
    #     return data
    
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user
    #     try:
    #         airline = validated_data.pop('airline')
    #         airticket = Airline.objects.create(passenger=user, **validated_data)
    #         airticket.airline.add(*airline)
    #     except:
    #         airticket = Airline.objects.create(passenger=user, **validated_data)

    #     return airticket

    
    

   
    
 





class CommentCreateSerializer(serializers.ModelSerializer):
    passenger = serializers.ReadOnlyField(source='passenger.name')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        comment = Comment.objects.create(passenger=user, **validated_data)
        return comment

class RatingSerializer(serializers.ModelSerializer):
    passenger = serializers.ReadOnlyField(source='passenger.name')
    class Meta:
        model = Rating
        fields = '__all__'

    def validate_rating(self, rating):
        if rating not in range(1,11):
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 10')
        return rating
        
    
    def create(self, validated_data):
        user = self.context.get('request').user
        rating = Rating.objects.create(passenger=user, **validated_data)
        return rating
    
    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)

    
    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user = request.user
    #     try:
    #         tags = validated_data.pop('tags')
    #         post = Airlines.objects.create(passenger=user,**validated_data)
    #         post.tags.add(*tags)
    #     except:
    #         post = Airlines.objects.create(passenger=user, **validated_data)
    #     return post
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['comments'] = instance.comments.count()
    #     # representation['rating'] = RatingSerializer(Rating.objects.filter(post=instance.pk), many=True).data
    #     representation['likes_count'] = instance.likes.count()
    #     representation['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
    #     return representation
