from django.urls import path
from . import views
# ONLY DEVELOPMENT
from django.conf import settings
from django.conf.urls.static import static


app_name = 'AppParts'
urlpatterns = [
    path('', views.marks_view, name='marks_view'),
    path('models/<int:mark_id>', views.models_view, name='models_view'),
    path('category/<int:model_id>', views.category_view, name='category_view'),
    path('part_detail/<int:part_id>', views.part_detail, name='part_detail'),
    path('get_parts/', views.get_parts, name='get_parts'),
    path('parts_search/', views.parts_search_view, name='parts_search'),
    path('disassembly/', views.disassembly, name='disassembly'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]

# ONLY DEVELOPMENT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


