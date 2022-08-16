from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from .models import Place


class StartPageView(View):
    def get(self, request, *args, **kwargs):
        places = Place.objects.all()
        features = []
        for place in places:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [place.lng, place.lat],
                },
                "properties": {
                    "title": place.title,
                    "placeId": f"place{place.id}",
                    "detailsUrl": reverse('place_url', args=(place.id,)),
                },
            })

        context = {
            'geojsonscript': {
                  "type": "FeatureCollection",
                  "features": features,
            },
        }
        return render(request, "index.html", context=context)


class PlaceView(View):
    def get(self, request, *args, **kwargs):
        place = get_object_or_404(Place, pk=kwargs['pk'])
        images = place.images.all().order_by('order')
        imgs = [img.picture.url for img in images]
        place_data = {
            "title": place.title,
            "imgs": imgs,
            "description_short": place.description_short,
            "description_long": place.description_long,
            "coordinates": {
                "lng": place.lng,
                "lat": place.lat,
            },
        }
        return JsonResponse(
            place_data,
            json_dumps_params={'ensure_ascii': False},
        )
