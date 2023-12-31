from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from PIL import Image
from datetime import date


class Marks(models.Model):
    mark_id = models.AutoField(primary_key=True)
    mark_name = models.CharField(max_length=20)
    image_url_mark = models.ImageField()
    # popular = models.BooleanField()

    def __str__(self):
        return self.mark_name

    class Meta:
        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'


class Models(models.Model):
    model_id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=20)
    image_url_model = models.ImageField()
    mark = models.ForeignKey(Marks, on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name

    class Meta:
        verbose_name = 'Model'
        verbose_name_plural = 'Models'


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    model = models.ManyToManyField(Marks)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Subcategories(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    subcategory_name = models.CharField(max_length=50)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory_name

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'


class Parts(models.Model):
    part_id = models.AutoField(primary_key=True)
    part_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50)
    image_url_part = models.ImageField(upload_to='part_media')
    additional_image_one = models.ImageField(upload_to='part_media', blank=True, null=True)
    additional_image_two = models.ImageField(upload_to='part_media', blank=True, null=True)
    additional_image_three = models.ImageField(upload_to='part_media', blank=True, null=True)
    availability = models.BooleanField(default=True)
    price = models.IntegerField()
    model = models.ManyToManyField(Models)
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE)

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
        return f'{self.part_name}'

    class Meta:
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'


class Disassembly(models.Model):
    disassembly_id = models.AutoField(primary_key=True)
    mark = models.ForeignKey(Marks, on_delete=models.CASCADE)
    model = models.ForeignKey(Models, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date = models.DateField(default=date.today)
    image_url_part = models.ImageField(upload_to='disassembly_media')
    additional_image_one = models.ImageField(upload_to='disassembly_media', blank=True, null=True)
    additional_image_two = models.ImageField(upload_to='disassembly_media', blank=True, null=True)
    additional_image_three = models.ImageField(upload_to='disassembly_media', blank=True, null=True)

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

    def __str__(self):
        return f'{self.disassembly_id}'

    class Meta:
        verbose_name = 'Disassembly'
        verbose_name_plural = 'Disassembly'



