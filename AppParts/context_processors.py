from .models import Categories


def categories_context(request):
    categories = Categories.objects.all()
    return {'categories': categories}
