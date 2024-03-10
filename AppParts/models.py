from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from PIL import Image
from datetime import date


class Marks(models.Model):
    mark_id = models.AutoField(primary_key=True)
    mark_name = models.CharField(max_length=20, verbose_name='Название')
    image_url_mark = models.ImageField(upload_to='mark_media', verbose_name='Изображение')

    def __str__(self):
        return self.mark_name

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'


class Models(models.Model):
    model_id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=20, verbose_name='Название')
    model_years = models.CharField(max_length=20, verbose_name='Годы')
    image_url_model = models.ImageField(upload_to='model_media', verbose_name='Изображение')
    mark = models.ForeignKey(Marks, on_delete=models.CASCADE, verbose_name='Марка')

    def __str__(self):
        return self.model_name

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, verbose_name='Название')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subcategories(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    subcategory_name = models.CharField(max_length=50, verbose_name='Название')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.subcategory_name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Parts(models.Model):
    part_id = models.AutoField(primary_key=True)
    part_name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    code = models.CharField(max_length=50, verbose_name='Артикул')
    image_url_part = models.ImageField(upload_to='part_media', verbose_name='Изображение')
    additional_image_one = models.ImageField(upload_to='part_media', blank=True, null=True,
                                             verbose_name='Дополнительное изображение')
    additional_image_two = models.ImageField(upload_to='part_media', blank=True, null=True,
                                             verbose_name='Дополнительное изображение')
    additional_image_three = models.ImageField(upload_to='part_media', blank=True, null=True,
                                               verbose_name='Дополнительное изображение')
    availability = models.BooleanField(default=True, verbose_name='Наличие')
    price = models.IntegerField(verbose_name='Цена')
    mark = models.ManyToManyField(Marks, verbose_name='Марки')
    model = models.ManyToManyField(Models, verbose_name='Модели')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, verbose_name='Подкатегория')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Обработка основного изображения
        img = Image.open(self.image_url_part.path)
        img = img.resize((1280, 960), Image.Resampling.LANCZOS)
        img.save(self.image_url_part.path)

        # Обработка дополнительных изображений
        for field_name in ['additional_image_one', 'additional_image_two', 'additional_image_three']:
            field = getattr(self, field_name)
            if field:
                img = Image.open(field.path)
                img = img.resize((1280, 960), Image.Resampling.LANCZOS)
                img.save(field.path)

    def formatted_price(self):
        return intcomma(self.price)

    def __str__(self):
        return self.part_name

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'


class Disassembly(models.Model):
    disassembly_id = models.AutoField(primary_key=True)
    mark = models.ForeignKey(Marks, on_delete=models.CASCADE, verbose_name='Марка')
    model = models.ForeignKey(Models, on_delete=models.CASCADE, verbose_name='Модель')
    description = models.TextField(blank=True, verbose_name='Описание')
    date = models.DateField(default=date.today, verbose_name='Дата разборки')
    image_url_car = models.ImageField(upload_to='disassembly_media', verbose_name='Изображение')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Обработка основного изображения
        img = Image.open(self.image_url_car.path)
        img = img.resize((1280, 960), Image.Resampling.LANCZOS)
        img.save(self.image_url_car.path)

    def __str__(self):
        return self.disassembly_id

    class Meta:
        verbose_name = 'Разборка'
        verbose_name_plural = 'Разборки'
