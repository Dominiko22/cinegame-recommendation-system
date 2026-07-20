from django.core.management.base import BaseCommand, CommandError

from recommender.services.tmdb import TmdbApiError, import_movie


class Command(BaseCommand):
    help = "Importuje film z TMDb po tytule."

    def add_arguments(self, parser):
        parser.add_argument("titles", nargs="+", type=str)
        parser.add_argument("--year", type=int, default=None)

    def handle(self, *args, **options):
        titles = options["titles"]
        year = options["year"]

        for title in titles:
            try:
                movie = import_movie(title, year=year)
            except TmdbApiError as error:
                raise CommandError(f"{title}: {error}") from error

            self.stdout.write(
                self.style.SUCCESS(
                    f"Zaimportowano film: {movie.title} ({movie.release_year})"
                )
            )
