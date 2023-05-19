from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category,Airline,AirTicket
from rest_framework.test import APIRequestFactory, force_authenticate,APITestCase
from .views import AirTicketViewSet

User = get_user_model()


class AirTicketTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(title='cat1')
        self.airline = Airline.objects.create(title='airline1')
        user = User.objects.create_user(email='user@gmail.com',password='12345', is_active=True,name='test')
        self.token = '12345'
        airtickets = [
            AirTicket(departure_city='new zealand', arrival_city='dubai1',category=self.category,departure_date ='2023-05-10',arrival_date='2023-12-12'),
            AirTicket(departure_city='new zealnad11',arrival_city='dubai2',category=self.category)
        ]
        AirTicket.objects.bulk_create(airtickets)

    def test_list(self):
        request =self.factory.get('api/v1/airticket/')
        view = AirTicketViewSet.as_view({'get': 'list'})
        response = view(request)


        assert response.status_code == 200
    
    # def test_create(self):
    #     user = User.objects.all()[0]
    #     data = {
    #         'departure_city': 'test',
    #         'arrival_city': 'bishkek1',
    #         'category': 'cat1',
            
    #     }
    #     request = self.factory.post('/airticket/',data,format='json')
    #     force_authenticate(request,user=user,token=self.token)
    #     view = AirTicketViewSet.as_view({'post': 'create'})
    #     response = view(request)
    #     # print(response)
         
    #     assert response.status_code == 201

    # def test_update(self):
    #     user = User.objects.all()[0]
    #     data = {
    #         'departure_city': 'updated departure_city'
    #     }
    #     airticket = AirTicket.objects.all()[1]
    #     request = self.factory.patch(f'/airticket/{airticket.id}/', data, format='json')
    #     force_authenticate(request, user=user)
    #     view = AirTicketViewSet.as_view({'patch': 'partial_update'})
    #     response = view(request, pk=airticket.id)
    #     print(response.data)
        
    #     assert AirTicket.objects.get(id=airticket.id).departure_city == data['departure_city']
    #     assert response.status_code == 200

   

    # def test_delete(self):
    #     user =  User.objects.all()[0]
    #     airticket = AirTicket.objects.all()[0]
    #     request = self.factory.delete(f'/airticket/{airticket.id}/')
    #     force_authenticate(request,user)
    #     view = AirTicketViewSet.as_view({'delete': 'destroy'})
    #     response = view(request, pk=airticket.id)
        

    #     assert response.status_code == 204
    #     assert not AirTicket.objects.filter(id=airticket.id).exists()

  

    # def test_retrieve(self):
    #     id = AirTicket.objects.all()[0].id
    #     request = self.factory.get(f'airticket/{id}/')
    #     view = AirTicketViewSet.as_view({'get': 'retrieve'})
    #     response = view(request,pk=id)
    #     print(response.data)

    #     assert response.status_code == 200
