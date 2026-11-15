from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from octofit_tracker import test_data
from octofit_tracker.models import Activity, Leaderboard, Team, User, Workout


class Command(BaseCommand):
    help = 'Delete existing data and populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Deleting through the ORM keeps the collections and their unique indexes
        for model in (Leaderboard, Activity, Team, Workout, User):
            model.objects.all().delete()

        users = {
            data['username']: User.objects.create(**{**data, 'password': make_password(data['password'])})
            for data in test_data.USERS
        }

        for name, usernames in test_data.TEAMS.items():
            team = Team.objects.create(name=name)
            team.members.set([users[username] for username in usernames], clear=True)

        for username, activity_type, duration in test_data.ACTIVITIES:
            Activity.objects.create(user=users[username], activity_type=activity_type, duration=duration)

        for username, score in test_data.LEADERBOARD:
            Leaderboard.objects.create(user=users[username], score=score)

        for name, description in test_data.WORKOUTS:
            Workout.objects.create(name=name, description=description)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
