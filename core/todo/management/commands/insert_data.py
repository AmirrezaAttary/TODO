from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from todo.models import Task
import random as R


class Command(BaseCommand):
    help = "inserting Damy Data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()


    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(), password="testpass")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraph(5)
        profile.save()
        print(f"User created: {user}")
        print(f"Your User Profile: {profile}")
        
        
        for _ in range(5):
            post = Task.objects.get_or_create(
                user = user,
                title = self.fake.sentence(nb_words=6),
                complete = R.choice([True,False])
            )
        print('Tost Created Successfully')
            