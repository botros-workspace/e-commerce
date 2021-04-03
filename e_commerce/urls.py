from django.conf import settings
from django.contrib import admin
from django.urls import path, include 
from core.views import checkout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace= 'core' )),
    path('checkout/', checkout, name ='check-out'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [ path('__debug__/', include(debug_toolbar.urls))   ]
    