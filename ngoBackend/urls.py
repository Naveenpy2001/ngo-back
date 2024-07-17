"""
URL configuration for ngoBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path


from app.views import SubmitContactForm,log_visit, get_visit_count

from app.views import SubmitContactForm,DonationCreateAPIView,index


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^.*$',index, name='index'),
    path('contact/',SubmitContactForm.as_view(),name='Contact-Form'),
    path('log_visit/', log_visit, name='log_visit'),
    path('get_visit_count/', get_visit_count, name='get_visit_count'),
]
