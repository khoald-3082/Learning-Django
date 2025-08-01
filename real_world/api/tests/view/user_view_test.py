from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from unittest.mock import patch, Mock

from ...models.article import Article
from ...models.comment import Comment
from ...serializers.user_serializer import UserSerializer

User = get_user_model()


class GetProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_staff=False,
        )

        # Create other user
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123',
            is_staff=False
        )

        # Generate JWT tokens
        self.user_refresh = RefreshToken.for_user(self.user)
        self.user_token = str(self.user_refresh.access_token)

        self.other_refresh = RefreshToken.for_user(self.other_user)
        self.other_token = str(self.other_refresh.access_token)

        # Create test articles and comments
        self.article1 = Article.objects.create(
            body='Test body 1',
            author=self.user,
            slug='test-article-1'
        )

        self.article2 = Article.objects.create(
            title='Test Article 2',
            body='Test body 2',
            author=self.user,
            slug='test-article-2'
        )

        self.comment1 = Comment.objects.create(
            body='Test comment 1',
            author=self.user,
            article=self.article1
        )

        self.url = reverse('api:user-detail')

    def test_authenticated_user_can_access_profile(self):
        """Test that authenticated user can access their profile"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['username'], self.user.username)
        self.assertEqual(response.data['profile']['email'], self.user.email)

        # Check articles and comments are included
        self.assertIn('articles', response.data)
        self.assertIn('comments', response.data)
        self.assertEqual(len(response.data['articles']), 2)
        self.assertEqual(len(response.data['comments']), 1)

    def test_unauthenticated_user_cannot_access_profile(self):
        """Test that unauthenticated user cannot access profile"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token_returns_401(self):
        """Test that invalid token returns 401"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_only_sees_own_articles_and_comments(self):
        """Test that user only sees their own articles and comments"""
        # Create article and comment for other user
        other_article = Article.objects.create(
            title='Other Article',
            body='Other body',
            author=self.other_user,
            slug='other-article'
        )

        Comment.objects.create(
            body='Other comment',
            author=self.other_user,
            article=other_article
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.get(self.url)

        # User should only see their own content
        self.assertEqual(len(response.data['articles']), 2)
        self.assertEqual(len(response.data['comments']), 1)

        # Check that other user's content is not included
        article_titles = [article['title'] for article in response.data['articles']]
        self.assertNotIn('Other Article', article_titles)


class RegisterUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api:user-register')

        self.valid_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
        }

    def test_successful_user_registration(self):
        """Test successful user registration"""
        response = self.client.post(self.url, self.valid_user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Register successful!')

        # Check user was created in database
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')

        # Check password was hashed
        self.assertTrue(check_password('testpass123', user.password))

    def test_registration_with_invalid_data(self):
        """Test registration with invalid data"""
        invalid_data = {
            'username': '',  # Empty username
            'email': 'invalid-email',  # Invalid email format
            'password': '123'  # Too short password
        }

        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_registration_with_missing_required_fields(self):
        """Test registration with missing required fields"""
        incomplete_data = {
            'username': 'testuser'
            # Missing email and password
        }

        response = self.client.post(self.url, incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_duplicate_username(self):
        """Test registration with duplicate username"""
        # Create existing user
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )

        duplicate_data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(self.url, duplicate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_duplicate_email(self):
        """Test registration with duplicate email"""
        # Create existing user
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='testpass123'
        )

        duplicate_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'testpass123'
        }

        response = self.client.post(self.url, duplicate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_registration_handles_serializer_save_exception(self):
        """Test that registration handles exceptions during serializer save"""
        # Use context manager instead of decorator
        with patch.object(UserSerializer, 'save', side_effect=Exception("Database save failed")):
            response = self.client.post(self.url, self.valid_user_data)

            # Should return BAD_REQUEST with error message
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('error_message', response.data)
            self.assertEqual(response.data['error_message'], "Database save failed")
