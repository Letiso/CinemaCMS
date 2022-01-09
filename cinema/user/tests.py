from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.


def create_default_users(new_users_count):
    user_model = get_user_model()
    users_to_create = []

    start_index = user_model.objects.last().id + 1
    end_index = start_index + new_users_count

    for index in range(start_index, end_index):
        users_to_create.append(
            user_model(
                username=f'test_user_{index}',
                email=f'test_email_{index}@gmail.com'
            )
        )

    user_model.objects.bulk_create(users_to_create)
