from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import models as app_models

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create teams
        teams = [
            {"name": "Team Marvel"},
            {"name": "Team DC"}
        ]
        team_ids = db.teams.insert_many(teams).inserted_ids

        # Create users
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": team_ids[0]},
            {"name": "Captain America", "email": "cap@marvel.com", "team": team_ids[0]},
            {"name": "Batman", "email": "batman@dc.com", "team": team_ids[1]},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": team_ids[1]},
        ]
        db.users.insert_many(users)
        db.users.create_index([("email", 1)], unique=True)

        # Create activities
        activities = [
            {"user": users[0]["email"], "activity": "Running", "duration": 30},
            {"user": users[1]["email"], "activity": "Cycling", "duration": 45},
            {"user": users[2]["email"], "activity": "Swimming", "duration": 60},
            {"user": users[3]["email"], "activity": "Yoga", "duration": 40},
        ]
        db.activities.insert_many(activities)

        # Create leaderboard
        leaderboard = [
            {"user": users[0]["email"], "points": 100},
            {"user": users[1]["email"], "points": 90},
            {"user": users[2]["email"], "points": 110},
            {"user": users[3]["email"], "points": 95},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Create workouts
        workouts = [
            {"user": users[0]["email"], "workout": "Pushups", "reps": 50},
            {"user": users[1]["email"], "workout": "Situps", "reps": 60},
            {"user": users[2]["email"], "workout": "Pullups", "reps": 30},
            {"user": users[3]["email"], "workout": "Squats", "reps": 70},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
