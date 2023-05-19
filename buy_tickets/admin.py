from django.contrib import admin
from .models import Category,AirTicket,Airline,Rating,Like,Comment,Favorite

admin.site.register(Category)
# admin.site.register(AirTicket)
admin.site.register(Airline)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Favorite)



class AirTicketAdmin(admin.ModelAdmin):
    list_display = ('departure_city', 'arrival_city', 'category','price')
    
    search_fields = ['departure_city', 'arrival_city']
    ordering = ['price']
    list_filter = ['category__title']

admin.site.register(AirTicket,AirTicketAdmin)
  