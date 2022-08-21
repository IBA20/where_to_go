from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    description_short = models.TextField(
        blank=True,
        verbose_name='Краткое Описание',
    )
    description_long = HTMLField(blank=True, verbose_name='Описание')
    lng = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        verbose_name='Долгота',
    )
    lat = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        verbose_name='Широта',
    )

    class Meta:
        unique_together = ['lng', 'lat']
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Локация',
    )
    order = models.IntegerField(default=0, verbose_name='Позиция')
    picture = models.ImageField(
        upload_to='images/%Y/%m/%d/',
        verbose_name='Картинка',
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    def __str__(self):
        return f'{self.order} {self.place}'
