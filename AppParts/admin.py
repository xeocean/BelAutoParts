from django.contrib import admin
from .models import Marks, Models, Categories, Subcategories, Parts, Disassembly


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['mark_name']
    ordering = ['mark_name']
    search_fields = ['mark_name']
    list_per_page = 50


@admin.register(Models)
class ModelsAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'mark']
    list_filter = ['mark']
    ordering = ['mark']
    filter = ['mark']
    search_fields = ['model_name_years']
    list_per_page = 50


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    ordering = ['category_name']
    search_fields = ['category_name']
    list_per_page = 50


@admin.register(Subcategories)
class SubcategoriesAdmin(admin.ModelAdmin):
    list_display = ['subcategory_name', 'category']
    list_filter = ['category']
    ordering = ['subcategory_name']
    search_fields = ['subcategory_name']
    list_per_page = 50


@admin.register(Parts)
class PartsAdmin(admin.ModelAdmin):
    list_display = ['part_name', 'code', 'availability', 'price', 'category', 'subcategory', 'display_mark',
                    'display_model']
    search_fields = ['part_name', 'code', 'category', 'subcategory']
    list_filter = ['category', 'subcategory', 'mark']
    list_editable = ['availability', 'price']
    ordering = ['code']
    list_per_page = 50

    class Media:
        js = ('js/parts_admin.js',)

    def display_model(self, obj):
        return ', '.join([str(model_instance) for model_instance in obj.model.all()])

    display_model.short_description = 'Модели'

    def display_mark(self, obj):
        return ', '.join([str(mark_instance) for mark_instance in obj.mark.all()])

    display_mark.short_description = 'Марки'


@admin.register(Disassembly)
class DisassemblyAdmin(admin.ModelAdmin):
    list_display = ['mark', 'model', 'date']
    search_fields = ['mark__mark_name', 'model__model_name']
    list_filter = ['mark']
    ordering = ['-date']
    list_per_page = 50
