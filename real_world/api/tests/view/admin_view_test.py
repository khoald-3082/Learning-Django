from urllib import response
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch, Mock, MagicMock

User = get_user_model()


class AdminViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Tạo admin user trong test database
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            is_staff=True,
        )
        self.admin_refresh = RefreshToken.for_user(self.admin)
        self.admin_token = str(self.admin_refresh.access_token)

        # Tạo regular user
        self.user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpass123',
            is_staff=False,
        )
        self.user_refresh = RefreshToken.for_user(self.user)
        self.user_token = str(self.user_refresh.access_token)

        self.url = reverse('api:admin-user-detail')

    def test_admin_can_access_profile(self):
        """Test that admin user can access their profile"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.admin.username)
        self.assertEqual(response.data['email'], self.admin.email)

    def test_user_cannot_access_admin_profile(self):
        """Test that user cannot access admin profile"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_access(self):
        """Test that unauthenticated user cannot access admin profile"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token_returns_401(self):
        """Test that invalid token returns 401"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_staff_user_can_access_profile(self):
        """Test that staff user (not superuser) can access profile"""
        staff_user = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='testpass123',
            is_staff=True,
        )

        staff_refresh = RefreshToken.for_user(staff_user)
        staff_token = str(staff_refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {staff_token}')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], staff_user.username)
