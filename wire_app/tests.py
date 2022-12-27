from wire_app.views import follow, like_post
from .models import FollowersCount, LikePost
from django.test import TestCase, Client
from .models import Profile, User, Post
from django.urls import reverse


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.profile = Profile.objects.create(
            user=self.user, id_user=1, bio='Test bio',
            location='Test location', profileimg='test_image.png'
        )

    def test_profile_creation(self):
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().bio, 'Test bio')

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'testuser')


class LikePostModelTestCase(TestCase):
    def setUp(self):
        self.like_post = LikePost.objects.create(
            post_id='12345', username='testuser'
        )

    def test_like_post_creation(self):
        self.assertEqual(LikePost.objects.count(), 1)
        self.assertEqual(LikePost.objects.get().post_id, '12345')

    def test_like_post_str(self):
        self.assertEqual(str(self.like_post), 'testuser')


class FollowersCountModelTestCase(TestCase):
    def setUp(self):
        self.followers_count = FollowersCount.objects.create(
            follower='testfollower', user='testuser'
        )

    def test_followers_count_creation(self):
        self.assertEqual(FollowersCount.objects.count(), 1)
        self.assertEqual(FollowersCount.objects.get().follower, 'testfollower')

    def test_followers_count_str(self):
        self.assertEqual(str(self.followers_count), 'testuser')


class SigninViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signin')
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )

    def test_signin_success(self):
        response = self.client.post(self.url, {
            'username': 'testuser', 'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_signin_failure(self):
        response = self.client.post(self.url, {
            'username': 'testuser', 'password': 'invalidpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/signin')


class SignupViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')

    def test_signup_success(self):
        response = self.client.post(self.url, {
            'username': 'testuser', 'email': 'test@example.com',
            'password': 'testpass', 'password2': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/settings')
        self.assertEqual(User.objects.count(), 1)

    def test_signup_failure_empty_password(self):
        response = self.client.post(self.url, {
            'username': 'testuser', 'email': 'test@example.com',
            'password': '', 'password2': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/signup')
        self.assertEqual(User.objects.count(), 0)

    def test_signup_failure_unmatching_passwords(self):
        response = self.client.post(self.url, {
            'username': 'testuser', 'email': 'test@example.com',
            'password': 'testpass', 'password2': 'invalidpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/signup')
        self.assertEqual(User.objects.count(), 0)

    def test_signup_failure_existing_email(self):
        User.objects.create_user(
            username='existinguser', email='test@example.com',
            password='testpass'
        )
        response = self.client.post(self.url, {
            'username': 'testuser', 'email': 'test@example.com',
            'password': 'testpass', 'password2': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/signup')
        self.assertEqual(User.objects.count(), 1)

    def test_signup_failure_existing_username(self):
        User.objects.create_user(
            username='testuser', email='existing@example.com',
            password='testpass'
        )
        response = self.client.post(self.url, {
            'username': 'testuser', 'email': 'test@example.com',
            'password': 'testpass', 'password2': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/signup')
        self.assertEqual(User.objects.count(), 1)


def test_like_post(request):
    # Test like post
    request.user = User.objects.create_user(username='user1')
    post = Post.objects.create(id=1, no_of_likes=0)
    request.GET = {'post_id': 1}
    response = like_post(request)
    post.refresh_from_db()
    assert post.no_of_likes == 1
    assert LikePost.objects.filter(post_id=1, username='user1').exists()
    assert response.status_code == 302  # redirect to '/'

    # Test unlike post
    request.user = User.objects.create_user(username='user1')
    post = Post.objects.create(id=2, no_of_likes=1)
    LikePost.objects.create(post_id=2, username='user1')
    request.GET = {'post_id': 2}
    response = like_post(request)
    post.refresh_from_db()
    assert post.no_of_likes == 0
    assert not LikePost.objects.filter(post_id=2, username='user1').exists()
    assert response.status_code == 302  # redirect to '/'


def test_follow(request):
    # Test follow
    request.method = 'POST'
    request.POST['follower'] = 'user1'
    request.POST['user'] = 'user2'
    response = follow(request)
    assert FollowersCount.objects.filter(
        follower='user1', user='user2').exists()
    assert response.status_code == 302  # redirect to '/profile/user2'

    # Test unfollow
    request.method = 'POST'
    request.POST['follower'] = 'user1'
    request.POST['user'] = 'user2'
    FollowersCount.objects.create(follower='user1', user='user2')
    response = follow(request)
    assert not FollowersCount.objects.filter(
        follower='user1', user='user2').exists()
    assert response.status_code == 302  # redirect to '/profile/user2'

    # Test GET request
    request.method = 'GET'
    response = follow(request)
    assert response.status_code == 302  # redirect to '/'
