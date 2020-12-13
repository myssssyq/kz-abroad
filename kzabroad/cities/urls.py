from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('<slug:city>',views.city, name='city'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
