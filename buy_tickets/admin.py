from django.contrib import admin
from .models import Category,AirTicket,Airline,Rating,Like,Comment

admin.site.register(Category)
admin.site.register(AirTicket)
admin.site.register(Airline)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Comment)
