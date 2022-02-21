from django.core.management.base import BaseCommand, CommandError

from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('new_users_count', type=int,
                            help="It's a count of test_users that'll be created by this command")

    def handle(self, *args, **options):
        user_model = get_user_model()
        users_to_create = []

        start_index = user_model.objects.last().id + 1
        end_index = start_index + options['new_users_count']

        for index in range(start_index, end_index):
            users_to_create.append(
                user_model(
                    username=f'test_user_{index}',
                    email=f'test_email_{index}@gmail.com'
                )
            )

        user_model.objects.bulk_create(users_to_create)
