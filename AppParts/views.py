import requests
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

from .forms import OrderForm
from .models import Marks, Models, Categories, Subcategories, Parts, Disassembly, Orders


def marks_view(request):
    marks = Marks.objects.all().order_by('mark_name')
    categories = Categories.objects.all()
    context = {'marks': marks, 'categories': categories}
    return render(request, 'AppParts/marks_view.html', context)


def models_view(request, mark_id):
    mark = get_object_or_404(Marks, mark_id=mark_id)
    models = Models.objects.filter(mark=mark)
    context = {'models': models, 'mark': mark}
    return render(request, 'AppParts/models_view.html', context)


def category_view(request, model_id):
    model = get_object_or_404(Models, model_id=model_id)
    categories = Categories.objects.all()
    subcategories = Subcategories.objects.all()
    context = {'categories': categories, 'subcategories': subcategories, 'model': model}
    return render(request, 'AppParts/category_view.html', context)


def part_detail(request, part_id):
    part = get_object_or_404(Parts, part_id=part_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Проверка CAPTCHA
            captcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': captcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                order_name = form.cleaned_data['order_name']
                order_phone = form.cleaned_data['order_phone']
                part_name = form.cleaned_data['part_name']
                part_code = form.cleaned_data['part_code']
                Orders.objects.create(order_name=order_name, order_phone=order_phone, part_name=part_name,
                                      part_code=part_code)
                message = 'Ваша заявка успешно отправлена!'
                # Возвращаем JSON с сообщением для обновления содержимого модального окна
                return JsonResponse({'message': message})
            else:
                # Если CAPTCHA не прошла, вы можете добавить соответствующее сообщение об ошибке
                message = 'Пожалуйста, пройдите проверку CAPTCHA.'
                return JsonResponse({'message': message}, status=400)
    else:
        OrderForm()
    context = {'part': part, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY}
    return render(request, 'AppParts/parts_detail.html', context)


def get_parts(request):
    selected_subcategories = request.GET.getlist('subcategory')
    selected_models = request.GET.getlist('model')
    model_id = request.GET.get('model_id')
    subcategory_id = request.GET.get('subcategory_id')
    sort_by = request.GET.get('sort')  # Получаем параметр сортировки

    if model_id:
        # Проверяем, есть ли значения 'subcategory_id'
        if not any(selected_subcategories):
            # Если нет, возвращаем все детали
            parts = Parts.objects.filter(model__model_id=model_id)
        else:
            # Если есть значения 'subcategory_id', продолжаем с фильтрацией
            parts = Parts.objects.filter(subcategory__in=selected_subcategories, model__model_id=model_id)

    elif subcategory_id:
        # Проверяем, есть ли значения 'model_id'
        if not any(selected_models):
            # Если нет, возвращаем все детали
            parts = Parts.objects.filter(subcategory__subcategory_id=subcategory_id)
        else:
            # Если есть значения 'model_id', продолжаем с фильтрацией
            parts = Parts.objects.filter(model__in=selected_models, subcategory__subcategory_id=subcategory_id)

    else:
        # Если отсутствуют идентификаторы, возвращаем пустой результат
        return JsonResponse({'parts_html': ''})

    # Добавляем логику для сортировки
    if sort_by == 'price_asc':
        parts = parts.order_by('price')
    elif sort_by == 'price_desc':
        parts = parts.order_by('-price')
    elif sort_by == 'name_asc':
        parts = parts.order_by('part_name')
    elif sort_by == 'name_desc':
        parts = parts.order_by('-part_name')

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

    # Количество элементов на одной странице
    items_per_page = 12
    paginator = Paginator(disassembly_list, items_per_page)
    page = request.GET.get('page')

    try:
        disassembly_list = paginator.page(page)
    except PageNotAnInteger:
        # Если параметр страницы не является целым числом, возвращаем первую страницу.
        disassembly_list = paginator.page(1)
    except EmptyPage:
        # Если страница находится за пределами допустимых значений, возвращаем последнюю страницу.
        disassembly_list = paginator.page(paginator.num_pages)
    context = {'disassembly_list': disassembly_list, }
    return render(request, 'AppParts/disassembly.html', context)


def contact(request):
    return render(request, 'AppParts/contact.html')


def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategories.objects.filter(category_id=category_id)
    data = {subcategory.subcategory_id: subcategory.subcategory_name for subcategory in subcategories}
    return JsonResponse(data)


def get_models(request):
    mark_ids = request.GET.getlist('mark_id[]')
    models = Models.objects.filter(mark_id__in=mark_ids)
    data = {model.model_id: model.model_name for model in models}
    return JsonResponse(data)


def get_models_disassembly(request):
    mark_id = request.GET.get('mark_id')
    models = Models.objects.filter(mark_id=mark_id)
    data = {model.model_id: model.model_name for model in models}
    return JsonResponse(data)


def get_subcategories_nav(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategories.objects.filter(category_id=category_id)
    subcategory_data = [{'id': subcategory.subcategory_id, 'name': subcategory.subcategory_name} for subcategory in
                        subcategories]
    return JsonResponse({'subcategories': subcategory_data})


# --------------------------------


def catalog_view(request, subcategory_id):
    subcategory = get_object_or_404(Subcategories, subcategory_id=subcategory_id)
    marks = Marks.objects.order_by('mark_name')
    models = Models.objects.order_by('model_name')
    context = {'subcategories': subcategory, 'marks': marks, 'models': models}
    return render(request, 'AppParts/catalog_view.html', context)

# --------------------------------
