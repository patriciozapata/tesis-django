from django.contrib import admin
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from foro.models import Topico,Comentario,Categoria,Post,Like

admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Comentario)
admin.site.register(Categoria)
admin.site.register(Topico)
