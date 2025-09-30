from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from parclick.views import welcome_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_page, name='welcome'),
    path('client/', include('client_app.urls')),
    path('employee/', include('employee_app.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
