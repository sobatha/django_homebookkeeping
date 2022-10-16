from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings
from kakeibo.urls import router as kakeibo_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("kakeibo/", include("kakeibo.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/", include(kakeibo_router.urls)),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
