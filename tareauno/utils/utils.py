import requests
import traceback
import pytz
from datetime import datetime
from django.db import transaction
from chr import settings
from tareauno.models import Network, Company, Payment_Types, Station, Location

def to_timezone(date_time, zone):
    timezone = pytz.timezone(zone)
    without_timezone = datetime.fromtimestamp(date_time)
    return timezone.localize(without_timezone)


def populate_station(stations, network):

    for station in stations:
        try:
            payment_types = []
            for payment in station['extra']['payment']:
                p, pt_created = Payment_Types.objects.get_or_create(
                    name=payment
                )
                payment_types.append(p)
            
            last_updated = to_timezone(station['extra']['last_updated'], "America/Santiago")
            
            station_obj, st_create = Station.objects.get_or_create(
                external_id=station['id'],
                defaults={
                    'name': station['name'] if 'name' in station else None,
                    'empty_slots': station['empty_slots'] if 'empty_slots' in station else None,
                    'free_bikes': station['free_bikes'] if 'free_bikes' in station else None,
                    'latitude': station['latitude'] if 'latitude' in station else 0.00,
                    'longitude': station['longitude'] if 'longitude' in station else 0.00,
                    'timestamp': station['timestamp'] if 'timestamp' in station else None,
                    'network': network,
                    'address': station['extra']['address'] if 'address' in station['extra'] else None,
                    'altitude': station['extra']['altitude'] if 'altitude' in station['extra'] else None,
                    'ebikes': station['extra']['ebikes'] if 'ebikes' in station['extra'] else None,
                    'has_ebikes': station['extra']['has_ebikes'] if 'has_ebikes' in station['extra'] else False,
                    'last_updated': last_updated,
                    'normal_bikes': station['extra']['normal_bikes'] if 'normal_bikes' in station['extra'] else None,
                    'payment_terminal': station['extra']['payment-terminal'] if 'payment-terminal' in station['extra'] else False,
                    'post_code': station['extra']['post_code'] if 'post_code' in station['extra'] else None,
                    'renting': station['extra']['renting'] if 'renting' in station['extra'] else None,
                    'returning': station['extra']['returning'] if 'returning' in station['extra'] else None,
                    'slots': station['extra']['slots'] if 'slots' in station['extra'] else None,
                    'uid': station['extra']['uid'] if 'uid' in station['extra'] else None,
                }
            )

            for pt in payment_types:
                station_obj.payment.add(pt)
        except Exception as e:
            print("{} {}".format("[STATION]", e))
            traceback.print_exc()
            pass


def request_api():
    sUrl = settings.API_URL
    response = requests.get("{}/{}".format(sUrl, 'networks/bikesantiago'))
    if response.status_code in [200, 201]:
        rjson = response.json()
        if "network" in rjson:
            try:
                with transaction.atomic():
                    network = rjson["network"]
                    if network['id']:
                        if 'location' in network and 'city' in network['location'] and 'country' in network['location']:
                            location, lct_create = Location.objects.get_or_create(
                                city=network['location']['city'],
                                country=network['location']['country'],
                                defaults={
                                    'latitude': network['location']['latitude'] if 'latitude' in network['location'] else None,
                                    'longitude': network['location']['longitude'] if 'longitude' in network['location'] else None,
                                }
                            )

                            companies = []
                            for c in network['company']:
                                company, cmp_create = Company.objects.get_or_create(
                                    name=c
                                )
                                companies.append(company)

                            network_obj, ntw_created = Network.objects.get_or_create(
                                external_id=network['id'],
                                defaults={
                                'name': network['name'] if 'name' in network else None,
                                'gbfs_href': network['gbfs_href'] if 'gbfs_href' in network else None,
                                'href': network['href'] if 'href' in network else None,
                                'external_id': network['id'] if 'id' in network else None,
                                'location': location
                            })

                            for company in companies:
                                network_obj.companies.add(company)
                            
                            if 'stations' in network:
                                populate_station(network['stations'], network_obj)
                                
                            return True
            except Exception as e:
                print(e)
                traceback.print_exc()
    
    return False
