from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from adminsortable2.admin import SortableTabularInline, SortableAdminBase

from .models import Place, Image


class ImageInline(SortableTabularInline):
    model = Image
    extra = 1
    verbose_name = "Фотография"
    verbose_name_plural = "Фотографии"

    def get_preview(self):
        height = min(self.picture.height, 200)
        width = self.picture.width / self.picture.height * height
        return format_html(
            "{}",
            mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=self.picture.url,
                    height=height,
                    width=width,
                )
            ),
        )

    readonly_fields = [get_preview]
    fields = ('picture', get_preview, 'order')


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["title"].label = "Название"
        form.base_fields["description_short"].label = "Краткое описание"
        form.base_fields["description_long"].label = "Описание"
        form.base_fields["lng"].label = "Долгота"
        form.base_fields["lat"].label = "Широта"
        return form

    def title(self):
        return self.title

    title.short_description = 'Локация'
    list_display = (title,)
    inlines = [ImageInline, ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):

    def order(self):
        return self.order

    def picture(self):
        return self.picture

    def place(self):
        return self.place

    order.short_description = 'Позиция'
    picture.short_description = 'Картинка'
    place.short_description = 'Локация'
    list_display = (order, place, picture)
    ordering = ['place', 'order']
    list_filter = ('place',)
