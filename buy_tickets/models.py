from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60,primary_key=True,blank=True)

    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class Airline(models.Model):
    title = models.CharField(max_length=50,primary_key=True,)
    slug = models.SlugField(max_length=60,blank=True)
    

    def __str__(self):
        return  f' {self.id} {self.title}'
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save()


class AirTicket(models.Model):
    passenger = models.ForeignKey(User,on_delete=models.CASCADE, related_name='airtickets',verbose_name='Пассажир')
    departure_city = models.CharField(max_length=50)
    arrival_city = models.CharField(max_length=50)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='airtickets')
    airline = models.ManyToManyField(Airline,related_name='airtickets')

    def __str__(self):
        return f'{self.departure_city} {self.arrival_city}'
    

# class BuyTickets(models.Model):
#     flight = models.ForeignKey(AirTickets, on_delete=models.CASCADE)
#     passenger = models.ForeignKey(User, on_delete=models.CASCADE)
#     seat_number = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     paid = models.BooleanField(default=False)

#     def __str__(self):
#         return f'{self.flight} {self.user}'



    

class Rating(models.Model):
    passenger = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ratings')
    rating = models.PositiveSmallIntegerField(default=0)
    airline = models.ForeignKey(Airline,on_delete=models.CASCADE,related_name='ratings')

    def __str__(self):
        return f' {self.rating} -> {self.airline}'
    
class Comment(models.Model):
    passenger = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    body = models.TextField()
    airline = models.ForeignKey(Airline,on_delete=models.CASCADE,related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.passenger.name} to {self.airline.title}'
    
class Like(models.Model):
    passenger = models.ForeignKey(User,on_delete=models.CASCADE, related_name='likes')
    airline = models.ForeignKey(Airline,on_delete=models.CASCADE,related_name='likes')
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'Liked {self.airline} by {self.passenger.name}'
    






