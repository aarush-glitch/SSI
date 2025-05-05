from django.contrib import admin
from django.urls import path, include
from .login import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index),
    path('nurse/', include('Nurse.urls')),
    path('junior_doctor/', include('JrDoctor.urls')),
    path('senior_doctor/', include('SrDoctor.urls')),
]