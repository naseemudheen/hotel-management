from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('admin/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('', include(('web.urls', 'web'), namespace='web')),
    path('accounts/', include(('account.urls', 'account'), namespace='account')),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

