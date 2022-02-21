from django.core.management.base import BaseCommand
from django.utils import timezone

from main.models import MovieSession, MovieCard, CinemaCard

from random import randint
from faker import Faker
import datetime

FAKE = Faker()


def get_random_element(elements_queryset) -> tuple:
    elements_tuple = tuple(elements_queryset)
    random_index = randint(1, len(elements_tuple))

    return elements_tuple[random_index - 1]


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument('new_movie_sessions_count', type=int,
                            help="It's a count of test_movie_sessions that'll be created by this command")

    @staticmethod
    def get_random_data() -> dict:
        movie_cards = MovieCard.objects.all()
        movie_card = get_random_element(movie_cards)

        movie_types = movie_card.get_movie_types_tuple()
        movie_type = get_random_element(movie_types)

        cinema = CinemaCard.objects.first()
        hall_cards = cinema.halls.all()
        hall_card = get_random_element(hall_cards)
        start = timezone.now()

        start_datetime = FAKE.date_time_between(start_date=start, end_date='+14d')
        start_datetime = timezone.make_aware(start_datetime)

        ticket_price = randint(45, 150)

        return {
            'movie': movie_card,
            'hall': hall_card,
            'movie_type': movie_type,
            'start_datetime': start_datetime,
            'ticket_price': ticket_price
        }

    def handle(self, *args, **options) -> None:
        movie_sessions_to_create = []

        end_index = options['new_movie_sessions_count']

        for session in range(end_index):
            random_data = self.get_random_data()

            movie_sessions_to_create.append(
                MovieSession(**random_data)
            )

        MovieSession.objects.bulk_create(movie_sessions_to_create)
