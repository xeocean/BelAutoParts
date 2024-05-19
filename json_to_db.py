import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BelAutoParts.settings")
django.setup()

from AppParts.models import Marks, Models

# Загрузка JSON данных
with open('to_db_2.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Создаем и сохраняем объекты Marks
marks_list = []
for mark_data in json_data:
    mark = Marks(
        mark_name=mark_data['mark_name'],
        image_url_mark=mark_data['image_url_mark'],
    )
    marks_list.append(mark)

# Сохраняем объекты Marks в базу данных
Marks.objects.bulk_create(marks_list)

# Получаем сохраненные объекты Marks из базы данных
saved_marks = {mark.mark_name: mark for mark in Marks.objects.all()}

# Создаем объекты Models, используя сохраненные объекты Marks
models_list = []
for mark_data in json_data:
    mark = saved_marks[mark_data['mark_name']]
    for model_data in mark_data['models']:
        model = Models(
            model_name=model_data['model_name'],
            image_url_model=model_data['image_url_model'],
            mark=mark,
        )
        models_list.append(model)

# Сохраняем объекты Models в базу данных
Models.objects.bulk_create(models_list)
