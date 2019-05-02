from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth import views as v
from django.conf.urls import handler404,handler500

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'foro/', include('foro.urls')),
    path(r'repositorio/', include('repositorio.urls')),
    path(r'conversor/', include('conversor.urls')),
    path(r'mapa/', include('carto.urls')),
    url(r'^reset/password_reset', password_reset, {'template_name':'registration/password_reset_form.html','email_template_name': 'registration/password_reset_email.html'},name='password_reset'),
    url(r'^password_reset_done', password_reset_done,{'template_name': 'registration/password_reset_done.html'},name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,{'template_name': 'registration/password_reset_confirm.html'},name='password_reset_confirm'),
    url(r'^reset/done', password_reset_complete, {'template_name': 'registration/password_reset_complete.html'},name='password_reset_complete'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
handler404 = 'foro.views.error_404_view'
handler500 = 'foro.views.error_500'
