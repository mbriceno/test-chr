import traceback
from django.core.management.base import BaseCommand, CommandError
from tareauno.utils.utils import request_api

class Command(BaseCommand):
    help = 'Comando para consultar el API Bike Santiago de la Tarea 1'

    def handle(self, *args, **options):
        """
        Method to invoke function to process API data
        """
        try:
            if request_api():
                print("Well Done!")
            else:
                print("No information in API")
        except Exception as e:
            traceback.print_exc()
        return False