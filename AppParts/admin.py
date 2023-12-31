from django.contrib import admin
from .models import Marks, Models, Categories, Subcategories, Parts, Disassembly


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['mark_id', 'mark_name', 'image_url_mark']
    ordering = ['mark_name']
    search_fields = ['mark_name']


@admin.register(Models)
class ModelsAdmin(admin.ModelAdmin):
    list_display = ['model_id', 'model_name', 'image_url_model', 'mark']
    filter = ['mark']
    search_fields = ['model_name', 'mark']


@admin.register(Categories)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'category_name']
    ordering = ['category_name']
    search_fields = ['category_name', 'model']


@admin.register(Subcategories)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['subcategory_id', 'subcategory_name']
    ordering = ['subcategory_name']
    search_fields = ['category_name', 'category']


@admin.register(Parts)
class PartsAdmin(admin.ModelAdmin):
    list_display = ['part_id', 'part_name', 'code', 'image_url_part',
                    'availability', 'price', 'model', 'subcategory']
    search_fields = ['part_name', 'code']


@admin.register(Disassembly)
class DisassemblyAdmin(admin.ModelAdmin):
    list_display = ['disassembly_id', 'mark', 'model', 'date']
    search_fields = ['mark', 'model']
