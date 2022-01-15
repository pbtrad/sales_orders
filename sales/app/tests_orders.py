from django.test import TestCase
from django.contrib.auth.models import User
import json

test_user = {"username": "testuser", "password": "testpassword"}

class OrdersTest(TestCase):
    def setUp(self):
        new_user = User.objects.create(
            username=test_user["username"])
        new_user.set_password(test_user["password"])
        new_user.save()

    def get_token(self):
        res = self.client.post('/api/token',
           data=json.dumps({
               'username': test_user["username"],
               'password': test_user["password"],
           }),
           content_type='application/json',
           )
        result = json.loads(res.content)
        self.assertTrue("access" in result)
        return result["access"]

    def test_add_orders_forbidden(self):
        res = self.client.post('/api/orders/',
        data=json.dumps({
            'date': "2022-01-01",
            'item': "Test Item",
            'price': 100,
            'quantity': 10,
        }),
        content_type='application/json',
        )
        self.assertEquals(res.status_code, 401)
        res = self.client.post('/api/orders',
        data=json.dumps({
            'date': "2022-01-01",
            'item': "Test Item",
            'price': 100,
            'quantity': 10,
        }),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Bearer WRONG TOKEN'
        )
        self.assertEquals(res.status_code, 401)

    def test_add_orders_ok(self):
        token = self.get_token()
        res = self.client.post('/api/orders/',
                              data=json.dumps({
                                  'date': "2022-01-01",
                                  'item': "Test Item",
                                  'price': 100,
                                  'quantity': 10,
                              }),
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Bearer {token}'
                              )
        self.assertEquals(res.status_code, 201)
        result = json.loads(res.content)["data"]
        self.assertEquals(result["date"], '2022-01-01')
        self.assertEquals(result["item"], 'Test Item')
        self.assertEquals(result["price"], '100')
        self.assertEquals(result["quantity"], '10')