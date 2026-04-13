from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# 🔥 DRF и JWT
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet
from users.views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# router для API
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),

    # твой сайт (НЕ ТРОГАЕМ)
    path('', include('catalog.urls')),
    path('posts/', include('posts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # 🔥 API (ДОБАВИЛИ)
    path('api/register/', RegisterView.as_view()),
    path('api/login/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    path('api/', include(router.urls)),
]

# медиа (картинки)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)