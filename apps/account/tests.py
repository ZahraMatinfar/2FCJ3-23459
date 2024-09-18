from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class AuthViewSetTests(APITestCase):
    
    def setUp(self):
        # Set up any initial data needed for the tests
        self.register_url = reverse('auth-register')  
        self.login_url = reverse('auth-login') 
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'strongpassword123'
        }

    def test_register_user(self):
        """
        Ensure we can register a new user successfully.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
    
    def test_register_user_invalid_data(self):
        """
        Test registration with invalid data (e.g., missing password).
        """
        invalid_data = {
            'email': 'invalid@example.com',
            # Password is missing
        }
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_user(self):
        """
        Ensure we can log in an existing user.
        """
        # First, register a user
        user = User.objects.create_user(
            email=self.user_data['email'], 
            password=self.user_data['password'],
        )
        Token.objects.create(user=user)
        
        # Now, attempt login
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_login_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        # Register a user
        User.objects.create_user(
            email=self.user_data['email'], 
            password=self.user_data['password']
        )
        
        # Attempt to login with an incorrect password
        login_data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_user_not_found(self):
        """
        Test login when the user does not exist.
        """
        # Attempt to login with non-existing user credentials
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'irrelevantpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
