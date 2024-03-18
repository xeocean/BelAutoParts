from .models import Categories

# Вывод на index
def categories_context(request):
    categories = Categories.objects.all()
    return {'categories': categories}
