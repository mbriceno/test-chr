import requests
import traceback
import pytz
from datetime import datetime
from django.db import transaction
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from chr import settings
from tareados.models import Project

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By


def scraper_url(pages):
    """
    Funcionalidad que hace uso de selenium para explorar la url solicitada, 
    busca las columnas de la tabla haciendo uso de xpath y crea o actualiza la info en la db.
    Arguments:
        pages: integer, numero de paginas que va recorrer el scraper
    Returns:
        boolean: boolean, True que indica que el scraper termino sin problemas, False en caso contrario
    """
    if pages > 0:
        try:
            # Configuracion de chrome para evitar uso excesivo de recursos y por tanto timeout al ejecutar scraper
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--window-size=1420,1080')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')

            # Configuración de path de chromedriver
            driver_path = "{}{}/chromedriver".format(settings.BASE_DIR_ALT, settings.STATIC_ROOT)
            
            service = ChromeService(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, chrome_options=chrome_options)

            for page in range(1, pages+1):
                sUrl = "{}?_paginador_refresh=1&_paginador_fila_actual={}".format(settings.SCRAPER_PAGE_URL, page)
                driver.get(sUrl)
                rows = driver.find_element(By.XPATH, "//table[@class='tabla_datos']/tbody/tr")
                cols = driver.find_element(By.XPATH, "//*[@class='tabla_datos']/tbody/tr[8]/td")
                
                for i in range(1, len(rows) + 1):
                    data = []
                    for j in range(1, len(cols) + 1):
                        data.append(driver.find_element_by_xpath ("//tr["+str(i)+"]/td["+str(j)+"]").text)
                    try:
                        with transaction.atomic():
                            date_time_obj = datetime.strptime(data[7], '%d/%m/%y')
                            date_income = date_time_obj.date
                            Project.objects.update_or_create(
                                external_id=data[0],
                                defaults={
                                    'name': data[1],
                                    'type': data[2],
                                    'region': data[3],
                                    'typology': data[4],
                                    'owner': data[5],
                                    'investment': float(data[6]),
                                    'date_income': date_income,
                                    'status': data[8]
                                }
                            )
                    except Exception as e:
                        pass
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
    return False
