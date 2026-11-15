"""Test data for the OctoFit Tracker database (Mergington High School)."""

from datetime import timedelta

USERS = [
    {'username': 'thundergod', 'email': 'thundergod@mhigh.edu', 'password': 'thundergodpassword'},
    {'username': 'metalgeek', 'email': 'metalgeek@mhigh.edu', 'password': 'metalgeekpassword'},
    {'username': 'zerocool', 'email': 'zerocool@mhigh.edu', 'password': 'zerocoolpassword'},
    {'username': 'crashoverride', 'email': 'crashoverride@hmhigh.edu', 'password': 'crashoverridepassword'},
    {'username': 'sleeptoken', 'email': 'sleeptoken@mhigh.edu', 'password': 'sleeptokenpassword'},
]

# Team name -> usernames of its members
TEAMS = {
    'Blue Team': ['thundergod', 'metalgeek', 'zerocool'],
    'Gold Team': ['crashoverride', 'sleeptoken'],
}

# (username, activity type, duration)
ACTIVITIES = [
    ('thundergod', 'Cycling', timedelta(hours=1)),
    ('metalgeek', 'Crossfit', timedelta(hours=2)),
    ('zerocool', 'Running', timedelta(hours=1, minutes=30)),
    ('crashoverride', 'Strength', timedelta(minutes=30)),
    ('sleeptoken', 'Swimming', timedelta(hours=1, minutes=15)),
]

# (username, score)
LEADERBOARD = [
    ('thundergod', 100),
    ('metalgeek', 90),
    ('zerocool', 95),
    ('crashoverride', 85),
    ('sleeptoken', 80),
]

# (name, description)
WORKOUTS = [
    ('Cycling Training', 'Training for a road cycling event'),
    ('Crossfit', 'Training for a crossfit competition'),
    ('Running Training', 'Training for a marathon'),
    ('Strength Training', 'Training for strength'),
    ('Swimming Training', 'Training for a swimming competition'),
]
