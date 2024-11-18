from django.contrib import admin
from django.urls import path
from bands.views import home, eventos, bandas, evento_form, register_banda, edit_banda, cancelar_registro_banda, get_students

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('eventos', eventos, name='eventos'),
    path('bandas', bandas, name='bandas'),    
    path('evento_form', evento_form, name='evento_form'),
    path('register_banda', register_banda, name='register_banda'),
    path('edit_banda/<int:banda_id>', edit_banda, name='editar_banda'),
    path('cancelar', cancelar_registro_banda, name='cancelar_registro_banda'),
    path('get_students', get_students, name='get_students'),
]
