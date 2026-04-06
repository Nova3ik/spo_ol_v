from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from app import views as app_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("favicon.ico", app_views.favicon, name="favicon"),
    path("", include("app.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__preview__/errors/400/", TemplateView.as_view(template_name="400.html"), name="preview_error_400"),
        path("__preview__/errors/403/", TemplateView.as_view(template_name="403.html"), name="preview_error_403"),
        path("__preview__/errors/404/", TemplateView.as_view(template_name="404.html"), name="preview_error_404"),
        path("__preview__/errors/500/", TemplateView.as_view(template_name="500.html"), name="preview_error_500"),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
