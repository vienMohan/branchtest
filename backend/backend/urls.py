from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from vien.views import *  # ✅ Import only what you need

router = routers.DefaultRouter()
router.register('candidates', EmpViewSet, basename='empviewset')
router.register('company', CompanyViewSet)
router.register('openings', OpeningViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    # DRF ViewSet for form submission
    path('api/', include(router.urls)),

    # Include OTP and other views like send-phone-otp
    path('auth/', include('vien.urls')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
