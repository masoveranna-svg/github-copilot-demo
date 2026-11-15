from datetime import timedelta

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Activity, Leaderboard, Team, User, Workout


class OctofitTestCase(TestCase):
    def setUp(self):
        for model in (Leaderboard, Activity, Team, Workout, User):
            model.objects.all().delete()
        self.client = APIClient()
        self.user = User.objects.create(
            username='thundergod', email='thundergod@mhigh.edu', password='secret'
        )


class ApiRootTests(OctofitTestCase):
    def test_api_root_lists_all_endpoints(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(response.data), {'users', 'teams', 'activities', 'leaderboard', 'workouts'}
        )


class UserTests(OctofitTestCase):
    def test_list_users_hides_password(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['email'], 'thundergod@mhigh.edu')
        self.assertNotIn('password', response.data[0])

    def test_create_user(self):
        response = self.client.post(
            '/api/users/',
            {'username': 'metalgeek', 'email': 'metalgeek@mhigh.edu', 'password': 'pw'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email='metalgeek@mhigh.edu').count(), 1)

    def test_email_must_be_unique(self):
        response = self.client.post(
            '/api/users/',
            {'username': 'copycat', 'email': 'thundergod@mhigh.edu', 'password': 'pw'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TeamTests(OctofitTestCase):
    def test_create_team_with_members(self):
        response = self.client.post(
            '/api/teams/',
            {'name': 'Blue Team', 'members': [str(self.user.pk)]},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['members'], [str(self.user.pk)])

    def test_list_teams(self):
        Team.objects.create(name='Gold Team')
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Gold Team')


class ActivityTests(OctofitTestCase):
    def test_create_activity(self):
        response = self.client.post(
            '/api/activities/',
            {'user': str(self.user.pk), 'activity_type': 'Cycling', 'duration': '01:00:00'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.get().duration, timedelta(hours=1))

    def test_activity_rejects_invalid_user_id(self):
        response = self.client.post(
            '/api/activities/',
            {'user': 'not-an-id', 'activity_type': 'Running', 'duration': '00:30:00'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LeaderboardTests(OctofitTestCase):
    def test_leaderboard_includes_username(self):
        Leaderboard.objects.create(user=self.user, score=100)
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], 'thundergod')
        self.assertEqual(response.data[0]['score'], 100)


class WorkoutTests(OctofitTestCase):
    def test_create_and_list_workout(self):
        response = self.client.post(
            '/api/workouts/',
            {'name': 'Swimming Training', 'description': 'Training for a swimming competition'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)
        listing = self.client.get('/api/workouts/')
        self.assertEqual(listing.data[0]['name'], 'Swimming Training')
