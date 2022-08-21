from django.contrib import admin
from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableTabularInline, SortableAdminBase

from .models import Place, Image


class ImageInline(SortableTabularInline):
    model = Image
    extra = 1
    verbose_name = "Фотография"
    verbose_name_plural = "Фотографии"

    @staticmethod
    def get_preview(image):
        height = min(image.picture.height, 200)
        width = image.picture.width / image.picture.height * height

        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=image.picture.url,
                height=height,
                width=width,
            ),
        )

    readonly_fields = ['get_preview']
    fields = ('picture', 'get_preview', 'order')


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title',)
    inlines = [ImageInline, ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('order', 'place', 'picture')
    ordering = ['place', 'order']
    list_filter = ('place',)
