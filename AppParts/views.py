from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from .models import Marks, Models, Categories, Subcategories, Parts, Disassembly


def marks_view(request):
    marks = Marks.objects.all().order_by('mark_name')
    context = {'marks': marks}
    return render(request, 'AppParts/marks_view.html', context)


def models_view(request, mark_id):
    mark = get_object_or_404(Marks, mark_id=mark_id)
    models = Models.objects.filter(mark=mark)
    context = {'models': models, 'mark': mark}
    return render(request, 'AppParts/models_view.html', context)


def category_view(request, model_id):
    model = get_object_or_404(Models, model_id=model_id)
    categories = Categories.objects.filter(model=model.mark)
    subcategories = Subcategories.objects.all()
    context = {'categories': categories, 'subcategories': subcategories, 'model': model}
    return render(request, 'AppParts/category_view.html', context)


def part_detail(request, part_id):
    part = get_object_or_404(Parts, part_id=part_id)
    context = {'part': part}
    return render(request, 'AppParts/parts_detail.html', context)


def get_parts(request):
    selected_subcategories = request.GET.getlist('subcategory')
    model_id = request.GET.get('model_id')

    # Проверяем, есть ли значения 'subcategory_id'
    if not any(selected_subcategories):
        # Если нет, возвращаем все детали
        parts = Parts.objects.filter(model__model_id=model_id)
    else:
        # Если есть значения 'subcategory_id', продолжаем с фильтрацией
        parts = Parts.objects.filter(subcategory__in=selected_subcategories, model__model_id=model_id)

    # Добавляем логику для пагинации
    items_per_page = 12
    page = request.GET.get('page', 1)
    paginator = Paginator(parts, items_per_page)  # Указываем количество элементов на странице
    try:
        parts = paginator.page(page)
    except PageNotAnInteger:
        parts = paginator.page(1)
    except EmptyPage:
        parts = paginator.page(paginator.num_pages)

    parts_html = render_to_string('AppParts/parts_partial.html', {'parts': parts})

    return JsonResponse({'parts_html': parts_html})


def parts_search_view(request):
    search_query = request.GET.get('search_query', '')
    parts = []

    if search_query:
        parts_list = Parts.objects.filter(
            Q(code__icontains=search_query) |
            Q(part_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

        # Количество элементов на одной странице
        items_per_page = 12
        paginator = Paginator(parts_list, items_per_page)
        page = request.GET.get('page')

        try:
            parts = paginator.page(page)
        except PageNotAnInteger:
            # Если параметр страницы не является целым числом, возвращаем первую страницу.
            parts = paginator.page(1)
        except EmptyPage:
            # Если страница находится за пределами допустимых значений, возвращаем последнюю страницу.
            parts = paginator.page(paginator.num_pages)

    return render(request, 'AppParts/parts_search.html', {'search_query': search_query, 'parts': parts})


def disassembly(request):
    disassembly_list = Disassembly.objects.all().order_by('-date')
    context = {'disassembly_list': disassembly_list}
    return render(request, 'AppParts/disassembly.html', context)


def contact(request):
    return render(request, 'AppParts/contact.html')


def about(request):
    return render(request, 'AppParts/about.html')
