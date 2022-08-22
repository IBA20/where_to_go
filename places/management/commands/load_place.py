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

    def get_place_data(self, json_link):
        response = get(json_link)
        if not response.ok:
            self.stdout.write(
                self.style.WARNING(f'File not found: {json_link}')
            )
            return
        try:
            place_data = response.json()
            place_data = PlaceSchema().load(place_data)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully retrieved data from {json_link}'
                )
            )
            return place_data
        except ValidationError as err:
            self.stdout.write(
                self.style.WARNING(f'Wrong data in: {json_link}')
            )
            for k, v in err.messages.items():
                self.stdout.write(self.style.WARNING(f'{k}: {v}'))
            return

    def download_images(self, n, img, place):
        filename = split(img)[1]
        img_response = get(img)
        if not img_response.ok:
            self.stdout.write(self.style.WARNING(f'Image not found: {img}'))
            return
        image = Image.objects.create(place=place, order=n)
        image.picture.save(
            filename,
            ContentFile(img_response.content),
            save=True
        )
        self.stdout.write(
            self.style.SUCCESS(f'Successfully retrieved image from {img}')
        )

    def handle(self, *args, **options):
        for json_link in options['json_links']:
            place_data = self.get_place_data(json_link)
            place, created = Place.objects.get_or_create(
                lng=place_data['lng'],
                lat=place_data['lat'],
                defaults={
                    'title': place_data['title'],
                    'description_short': place_data.get(
                        'description_short',
                        ''
                    ),
                    'description_long': place_data.get(
                        'description_long',
                        ''
                    ),
                }
            )
            if not created:
                self.stdout.write(
                    self.style.WARNING(f'Object already exists:{json_link}')
                )
                continue

            for n, img in enumerate(place_data.get('imgs', []), 1):
                self.download_images(n, img, place)
