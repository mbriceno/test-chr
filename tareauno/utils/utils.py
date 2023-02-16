import requests
import traceback
import pytz
from datetime import datetime
from django.db import transaction
from chr import settings
from tareauno.models import Network, Company, Payment_Types, Station, Location

def request_api():
    sUrl = settings.API_URL
    response = requests.get("{}/{}".format(sUrl, 'networks/bikesantiago'))
    if response.status_code in [200, 201]:
        rjson = response.json()
        if rjson["network"]:
            try:
                with transaction.atomic():
                    network = rjson["network"]
                    if network['id']:
                        if network['location'] and network['location']['city'] and network['location']['country']:
                            location, lct_create = Location.objects.get_or_create(
                                city=network['location']['city'],
                                country=network['location']['country'],
                                defaults={
                                    'latitude': network['location']['latitude'] if network['location']['latitude'] else None,
                                    'longitude': network['location']['longitude'] if network['location']['longitude'] else None,
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
                                'name': network['name'] if network['name'] else None,
                                'gbfs_href': network['gbfs_href'] if network['gbfs_href'] else None,
                                'href': network['href'] if network['href'] else None,
                                'external_id': network['id'] if network['id'] else None,
                                'location': location
                            })

                            for company in companies:
                                network_obj.companies.add(company)
                            
                            if network['stations']:
                                for station in network['stations']:
                                    try:
                                        payment_types = []
                                        for payment in station['extra']['payment']:
                                            p, pt_created = Payment_Types.objects.get_or_create(
                                                name=payment
                                            )
                                            payment_types.append(p)
                                        
                                        timezone = pytz.timezone("America/Santiago")
                                        last_updated = datetime.fromtimestamp(station['extra']['last_updated'])
                                        last_updated = timezone.localize(last_updated)
                                        
                                        station_obj, st_create = Station.objects.get_or_create(
                                            external_id=station['id'],
                                            defaults={
                                                'name': station['name'] if station['name'] else None,
                                                'empty_slots': station['empty_slots'] if station['empty_slots'] else None,
                                                'free_bikes': station['free_bikes'] if station['free_bikes'] else None,
                                                'latitude': station['latitude'] if station['latitude'] else 0.00,
                                                'longitude': station['longitude'] if station['longitude'] else 0.00,
                                                'timestamp': station['timestamp'] if station['timestamp'] else None,
                                                'network': network_obj,
                                                'address': station['extra']['address'] if station['extra']['address'] else None,
                                                'altitude': station['extra']['altitude'] if station['extra']['altitude'] else None,
                                                'ebikes': station['extra']['ebikes'] if station['extra']['ebikes'] else None,
                                                'has_ebikes': station['extra']['has_ebikes'] if station['extra']['has_ebikes'] else False,
                                                'last_updated': last_updated,
                                                'normal_bikes': station['extra']['normal_bikes'] if station['extra']['normal_bikes'] else None,
                                                'payment_terminal': station['extra']['payment-terminal'] if station['extra']['payment-terminal'] else False,
                                                'post_code': station['extra']['post_code'] if 'post_code' in station['extra'] else None,
                                                'renting': station['extra']['renting'] if station['extra']['renting'] else None,
                                                'returning': station['extra']['returning'] if station['extra']['returning'] else None,
                                                'slots': station['extra']['slots'] if station['extra']['slots'] else None,
                                                'uid': station['extra']['uid'] if station['extra']['uid'] else None,
                                            }
                                        )

                                        for pt in payment_types:
                                            station_obj.payment.add(pt)
                                    except Exception as e:
                                        print("{} {}".format("[STATION]", e))
                                        traceback.print_exc()
                                        pass
                            return True
            except Exception as e:
                print(e)
                traceback.print_exc()
    
    return False
