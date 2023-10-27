import os

from django.conf import settings
from django.db import models
from PIL import Image


class Product(models.Model):
    name = models.CharField(max_length=80)
    description_short = models.TextField(max_length=150)
    description_long = models.TextField(max_length=350)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    slug = models.SlugField(max_length=80, unique=True)
    price = models.FloatField()
    price_promo = models.FloatField(default=0)
    type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variation'),
            ('N', 'Simple')
        )
    )

    def resize_image(self, width=800):
        image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
        img = Image.open(image_path)
        img_width, img_height = img.size

        if img_width <= width:
            img.close()
            return

        new_width = width
        new_height = round((new_width * img_height) / img_width)

        new_img = img.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(image_path, optimize=True, quality=50)

    def save(self, *args, **kwargs):
        super().save(self, *args, **kwargs)

        if self.image:
            self.resize_image()

    def __str__(self):
        return str(self.name)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    price = models.FloatField()
    price_promo = models.FloatField(default=0)
    stock = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} - {self.name}'
