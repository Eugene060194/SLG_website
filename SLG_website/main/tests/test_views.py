from django.test import TestCase


class ViewsTests(TestCase):
    def test_index(self):
        response = self.client.get('http://127.0.0.1:8000/')
        self.assertEqual(response.status_code, 200)

    def test_authorization(self):
        response = self.client.get('http://127.0.0.1:8000/auth')
        self.assertEqual(response.status_code, 200)

    def test_logout_user(self):
        response = self.client.get('http://127.0.0.1:8000/logout')
        self.assertEqual(response.status_code, 302)

    def test_registration(self):
        response = self.client.get('http://127.0.0.1:8000/reg')
        self.assertEqual(response.status_code, 200)

    def test_examples(self):
        response = self.client.get('http://127.0.0.1:8000/textexamples')
        self.assertEqual(response.status_code, 200)

    def test_my_texts(self):
        response = self.client.get('http://127.0.0.1:8000/mytexts')
        self.assertEqual(response.status_code, 302)

    def test_generator(self):
        response = self.client.get('http://127.0.0.1:8000/generator')
        self.assertEqual(response.status_code, 200)
