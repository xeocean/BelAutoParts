import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BelAutoParts.settings")
django.setup()

from AppParts.models import Marks, Models

with open('to_db_2.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

marks_list = []
models_list = []

for mark_data in json_data:
    mark = Marks(
        mark_name=mark_data['mark_name'],
        image_url_mark=mark_data['image_url_mark'],
    )
    marks_list.append(mark)

    for model_data in mark_data['models']:
        model = Models(
            model_name=model_data['model_name'],
            image_url_model=model_data['image_url_model'],
            mark=mark,
        )
        models_list.append(model)

# Используйте bulk_create для эффективной вставки данных в базу данных
Marks.objects.bulk_create(marks_list)
Models.objects.bulk_create(models_list)

