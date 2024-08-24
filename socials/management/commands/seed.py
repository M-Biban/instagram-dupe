from django.core.management.base import BaseCommand, CommandError

from socials.models import User, Follower

import pytz
from faker import Faker
from random import randint, random
import random

user_fixtures = [
    {'username': 'johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': 'janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': 'charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]


class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 30
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'
    FRIEND_COUNT = 100

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.users = User.objects.all()
        self.try_create_followers()

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        user_count = User.objects.count()
        while  user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})
       
    def try_create_user(self, data):
        try:
            self.create_user(data)
        except:
            pass

    def create_user(self, data):
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        
    def get_random_user(self):
        index = random.randint(0, self.users.count() - 1)
        return self.users[index]
        
    """Create followers"""
    def try_create_followers(self):
        for i in range(self.FRIEND_COUNT):
            try:
                self.create_follower()
            except:
                print("Fail")
                pass
        print("Follower seeding complete.   ")
        
    def create_follower(self):
            follower = self.get_random_user()
            followee = self.get_random_user()
            print(follower.username)
            print(followee.username)
            Follower.objects.create(
                follower = follower,
                current_user = followee
            )
            
            

def create_username(first_name, last_name):
    return first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'
