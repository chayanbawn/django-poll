from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class TestApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "http://127.0.0.1:8000/api/values/"

    def test_get_all(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_store(self):
        response = self.client.post(self.uri, data='{"key1": "key 1 value", "key1": "key 2 value"}',
                                    content_type='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_update(self):
        response = self.client.patch(self.uri, data='{"key1": "key 1 updated value"}',
                                     content_type='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))

    def test_get_by_keys(self):
        response = self.client.get(self.uri, data={"keys": "key1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         'Expected Response Code 200, received {0} instead.'
                         .format(response.status_code))
