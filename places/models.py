from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=256)
    description_short = models.CharField(max_length=1024)
    description_long = HTMLField(blank=True)
    lng = models.DecimalField(max_digits=17, decimal_places=14)
    lat = models.DecimalField(max_digits=17, decimal_places=14)

    class Meta:
        unique_together = ['lng', 'lat']
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    order = models.IntegerField(default=0, verbose_name='Позиция', blank=False, null=False, db_index=True)
    src = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Картинка')

    class Meta:
        ordering = ['order']
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return str(self.order) + ' ' + str(self.place)