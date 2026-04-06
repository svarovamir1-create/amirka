from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # каталог (магазин)
    path('', include('catalog.urls')),

    # публикации
    path('posts/', include('posts.urls')),

    # авторизация
    path('accounts/', include('django.contrib.auth.urls')),
]

# медиа (картинки)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)