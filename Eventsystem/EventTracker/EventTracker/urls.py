
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('account.urls')),
    path('EventRecord/',include('EventRecord.urls')),
    path('administrator/',include('administrator.urls')),
    path('employee/',include('employee.urls')),
    path('tinymce/',include('tinymce.urls')),
    path('apis/',include('apis.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_title = 'Event Tracking System'
admin.site.site_header = 'Event Tracker'
admin.site.index_title = 'Event Tracker Adminstration'
