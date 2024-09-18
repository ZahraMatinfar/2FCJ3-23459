from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.pagination import PageNumberPagination
from apps.ads.models import Ad, Comment
from django.contrib.auth import get_user_model


User = get_user_model()


# class AdViewSetTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='user@example.com', password='password')
#         self.client.force_authenticate(user=self.user)
#         self.ad = Ad.objects.create(title='Test Ad', description='Test description', owner=self.user)

#     def test_create_ad(self):
#         url = reverse('ad-list')  # Adjust the URL if your name is different
#         data = {
#             'title': 'New Ad',
#             'description': 'Description of the new ad',
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Ad.objects.count(), 2)
#         self.assertEqual(Ad.objects.latest('id').title, 'New Ad')

#     def test_list_ads(self):
#         url = reverse('ad-list')  # Adjust the URL if your name is different
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         print(response.data)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['title'], 'Test Ad')

#     def test_ad_owner(self):
#         url = reverse('ad-list')  # Adjust the URL if your name is different
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data[0]['owner']['email'], self.user.email)


# class CommentViewSetTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='user@example.com', password='password')
#         self.ad = Ad.objects.create(title='Test Ad', description='Test description', owner=self.user)
#         self.client.force_authenticate(user=self.user)

#     def test_create_comment(self):
#         url = reverse('comments', kwargs={'ad_pk': self.ad.id})
#         data = {'text': 'This is a new comment'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Comment.objects.count(), 1)
#         self.assertEqual(Comment.objects.get().text, 'This is a new comment')

#     def test_list_comments(self):
#         Comment.objects.create(ad=self.ad, user=self.user, text='Existing comment')
#         url = reverse('comments', kwargs={'ad_pk': self.ad.id})
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['text'], 'Existing comment')

#     def test_create_comment_duplicate(self):
#         Comment.objects.create(ad=self.ad, user=self.user, text='Existing comment')
#         url = reverse('comments', kwargs={'ad_pk': self.ad.id})
#         data = {'text': 'Existing comment'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('You have already commented on this ad.', response.data['non_field_errors'])


class AdViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(email="user1@example.com", password="testpassword123")
        self.client.login(email="user1@example.com", password="testpassword123")

        self.non_owner_user = User.objects.create_user(email="user2@example.com", password="testpassword123")
        
        # Set up an ad for testing
        self.ad = Ad.objects.create(title="Test Ad", description="Test Description", owner=self.user)

    def test_create_ad(self):
        # Create an ad through the API
        url = reverse('ad-list')  # Assuming basename='ad' in DefaultRouter
        data = {
            "title": "New Ad",
            "description": "This is a new ad",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["owner"]["email"], self.user.email)

    def test_edit_ad(self):
        # Edit the existing ad
        url = reverse('ad-detail', kwargs={'pk': self.ad.pk})
        data = {
            "title": "Updated Ad",
            "description": "Updated description",
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Ad")

    def test_edit_ad_by_non_owner(self):
        # Login as a different user and try to edit the ad
        self.client.login(email="user2@example.com", password="testpassword123")
        url = reverse('ad-detail', kwargs={'pk': self.ad.pk})
        data = {"title": "Malicious Update"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_ad(self):
        # Delete the ad
        url = reverse('ad-detail', kwargs={'pk': self.ad.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())

    def test_delete_ad_by_non_owner(self):
        # Login as a different user and try to delete the ad
        self.client.login(email="user2@example.com", password="testpassword123")
        url = reverse('ad-detail', kwargs={'pk': self.ad.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_ad_list(self):
        # Get list of ads without being authenticated
        self.client.logout()
        url = reverse('ad-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data["results"]), PageNumberPagination.page_size)



class CommentTests(APITestCase):
    def setUp(self):
        # Create users and ads
        self.user1 = User.objects.create_user(email="user1@example.com", password="testpassword123")
        self.user2 = User.objects.create_user(email="user2@example.com", password="testpassword123")
        self.client.login(email="user1@example.com", password="testpassword123")
        self.ad = Ad.objects.create(title="Test Ad", description="Test Description", owner=self.user2)

    def test_create_comment(self):
        # Create a comment on an ad
        url = reverse('comments', kwargs={'ad_pk': self.ad.pk})
        data = {"text": "Nice ad!"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "Nice ad!")
        self.assertEqual(response.data["user"]["email"], self.user1.email)

    def test_unique_comment_per_user(self):
        # Ensure that a user can comment only once on the same ad
        url = reverse('comments', kwargs={'ad_pk': self.ad.pk})
        data = {"text": "First comment"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Try commenting again with the same user
        data = {"text": "Second comment"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You have already commented on this ad.", str(response.data))

    def test_get_comments(self):
        # Get list of comments for a specific ad
        Comment.objects.create(ad=self.ad, user=self.user1, text="Great ad!")
        Comment.objects.create(ad=self.ad, user=self.user2, text="Interesting!")
        
        url = reverse('comments', kwargs={'ad_pk': self.ad.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data["results"]), PageNumberPagination.page_size)
