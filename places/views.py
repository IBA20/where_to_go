from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Place, Image
from where_to_go import settings


class StartPageView(View):
    def get(self, request, *args, **kwargs):
        places = Place.objects.all()
        features = []
        for place in places:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(place.lng), float(place.lat)]
                },
                "properties": {
                    "title": place.title,
                    "placeId": 'place' + str(place.id),
                    "detailsUrl": "/places/" + str(place.id)
                    }
            })

        data = {
            'geojsonscript': {
                  "type": "FeatureCollection",
                  "features": features
                }
            }
        return render(request, "index.html", context=data)


class PlaceView(View):
    def get(self, request, *args, **kwargs):
        queryset = Image.objects.filter(place__id=self.kwargs['pk']).select_related().order_by('order')
        if not queryset:
            place = get_object_or_404(Place, pk=self.kwargs['pk'])
            imgs = []
        else:
            place = queryset[0].place
            imgs = [settings.MEDIA_URL + str(el.path) for el in queryset]
        data = {
            "title": place.title,
            "imgs": imgs,
            "description_short": place.description_short,
            "description_long": place.description_long,
            "coordinates": {
                "lng": place.lng,
                "lat": place.lat
            }
        }
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 2})
