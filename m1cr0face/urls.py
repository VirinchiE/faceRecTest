"""m1cr0face URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^detect/', include('detect_app.urls')),
  url(r'^teach/', include('teach_app.urls')),
  url(r'^newface/',include('newface_app.urls')),  
  url(r'^list/',include('detect_app.urls')),
  url(r'^deleteFace/',include('deleteface_app.urls')),
  url(r'^checkin_checkout/',include('checkin_checkout_app.urls')),
  url(r'^user_details/',include('user_details_app.urls')),
  url(r'^update_employee_code/',include('update_employee_code_app.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
  # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
