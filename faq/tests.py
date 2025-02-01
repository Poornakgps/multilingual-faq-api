from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import FAQ
from django.urls import reverse
from django.core.cache import cache

class FAQAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.faq = FAQ.objects.create(
            question_en="Test question?",
            answer_en="Test answer."
        )
        cache.clear()  # Clear cache before each test

    def test_create_faq(self):
        url = reverse('create_faq')
        data = {
            'question_en': 'New test question?',
            'answer_en': 'New test answer.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FAQ.objects.count(), 2)
        self.assertTrue('question_hi' in response.data)  # Check if translation was created

    def test_get_all_faqs(self):
        url = reverse('get_all_faqs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_faqs_by_language(self):
        url = reverse('get_faqs_by_language', kwargs={'lang': 'en'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], 'Test question?')

    def test_get_faq_by_language(self):
        url = reverse('get_faq_by_language', kwargs={'id': self.faq.id, 'lang': 'en'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], 'Test question?')

    def test_update_faq(self):
        url = reverse('update_faq', kwargs={'id': self.faq.id})
        data = {
            'question_en': 'Updated question?',
            'answer_en': 'Updated answer.'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.faq.refresh_from_db()
        self.assertEqual(self.faq.question_en, 'Updated question?')

    def test_delete_faq(self):
        url = reverse('delete_faq', kwargs={'id': self.faq.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FAQ.objects.count(), 0)

    def test_invalid_language(self):
        url = reverse('get_faqs_by_language', kwargs={'lang': 'invalid'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_faq_not_found(self):
        url = reverse('get_faq_by_language', kwargs={'id': 9999, 'lang': 'en'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_faq_invalid_data(self):
        url = reverse('create_faq')
        data = {'question_en': ''}  # Invalid data (empty question)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_faq_invalid_data(self):
        url = reverse('update_faq', kwargs={'id': self.faq.id})
        data = {'question_en': ''}  # Invalid data (empty question)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
