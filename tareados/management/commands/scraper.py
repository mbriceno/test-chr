import traceback
from django.core.management.base import BaseCommand, CommandError
from tareados.utils.utils import scraper_url

class Command(BaseCommand):
    help = 'Comando para consultar el API Bike Santiago de la Tarea 1'

    def add_arguments(self, parser):
        parser.add_argument('--pages', type=int)

    def handle(self, *args, **options):
        """
        Method to invoke function to process API data
        """
        try:
            pages = options.get('pages', 4)
            if scraper_url(pages):
                print("Well Done!")
            else:
                print("Some issues detected")
        except Exception as e:
            traceback.print_exc()
        return False