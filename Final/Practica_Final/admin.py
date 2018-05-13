from django.contrib import admin
from .models import Museo, Comentario, Pag_Usuario, Museo_Usuario

# Register your models here.
admin.site.register(Museo)
admin.site.register(Comentario)
admin.site.register(Pag_Usuario)
admin.site.register(Museo_Usuario)