import json

from decimal import Decimal
from requests import get
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from places.models import Place, Image


class Command(BaseCommand):
    help = 'Loads data from external GeoJSON'

    def add_arguments(self, parser):
        parser.add_argument('json_links', nargs='+', type=str)

    def handle(self, *args, **options):
        for json_link in options['json_links']:
            response = get(json_link)
            if not response.status_code == 200:
                self.stdout.write(self.style.WARNING('File not found: "%s"' % json_link))
            else:
                try:
                    place_data = json.loads(response.content)
                    self.stdout.write(self.style.SUCCESS('Successfully retrieved data from "%s"' % json_link))
                    place, created = Place.objects.get_or_create(lng=Decimal(place_data['coordinates']['lng']),
                                                                 lat=Decimal(place_data['coordinates']['lat']),
                                                                 defaults={'title': place_data['title'],
                                                                           'description_short': place_data['description_short'],
                                                                           'description_long': place_data['description_long']
                                                                           })
                except Exception:
                    self.stdout.write(self.style.WARNING('File  contains wrong data: "%s"' % json_link))
                    continue
                if not created:
                    self.stdout.write(self.style.WARNING('Object already exists: "%s"' % json_link))
                else:
                    for n, img in enumerate(place_data['imgs']):
                        filename = img.split('/')[-1]
                        imgfile = get(img)
                        if not imgfile.status_code == 200:
                            self.stdout.write(self.style.WARNING('Image not found: "%s"' % img))
                        else:
                            image = Image.objects.create(place=place, order=n + 1)
                            image.src.save(filename, ContentFile(imgfile.content), save=True)
                            self.stdout.write(self.style.SUCCESS('Successfully retrieved image from "%s"' % img))
