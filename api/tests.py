from django.test import TestCase
from api.models import User, Order
from django.urls import reverse
from rest_framework import status

# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='test')
        user2 = User.objects.create_user(username='user2', password='test')
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)
    
    def test_user_order_endpoint_retrievs_only_authenticated_user_order(self):
        user = User.objects.get(username='user1')
        self.client.force_login(user)
        response = self.client.get(reverse('user-orders'))

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()

        '''We'er getting response and for each res we'er looking for 
        ID verification that we have selected above(line 16)'''
        self.assertTrue(all(order['user'] == user.id for order in orders))


    def test_user_order_list_unauthenticated(self):
        ''' If unauthenticated it should only return 403 if any other
        response is retured then there might be some different error '''

        response = self.client.get(reverse('user-orders'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
