from decimal import Decimal
from os.path import split
from marshmallow import ValidationError
from requests import get
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from ._schemes import PlaceSchema
from places.models import Place, Image


class Command(BaseCommand):
    help = 'Loads data from external JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_links', nargs='+', type=str)

    def handle(self, *args, **options):
        for json_link in options['json_links']:
            response = get(json_link)
            if not response.ok:
                self.stdout.write(
                    self.style.WARNING(f'File not found: {json_link}')
                )
                continue
            try:
                place_data = response.json()
                PlaceSchema().load(place_data)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully retrieved data from {json_link}'
                    )
                )
                place, created = Place.objects.get_or_create(
                    lng=Decimal(place_data['coordinates']['lng']),
                    lat=Decimal(place_data['coordinates']['lat']),
                    defaults={
                        'title': place_data['title'],
                        'description_short': place_data['description_short'],
                        'description_long': place_data['description_long'],
                    }
                )
            except ValidationError as err:
                self.stdout.write(
                    self.style.WARNING(f'Wrong data in: {json_link}')
                )
                for k, v in err.messages.items():
                    self.stdout.write(self.style.WARNING(f'{k}: {v}'))
                continue
            if not created:
                self.stdout.write(
                    self.style.WARNING(f'Object already exists:{json_link}')
                )
                continue
            for n, img in enumerate(place_data['imgs']):
                filename = split(img)[1]
                imgfile = get(img)
                if not imgfile.ok:
                    self.stdout.write(
                        self.style.WARNING(f'Image not found: {json_link}')
                    )
                    continue
                image = Image.objects.create(place=place, order=n + 1)
                image.picture.save(
                    filename,
                    ContentFile(imgfile.content),
                    save=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully retrieved image from {json_link}'
                    )
                )
