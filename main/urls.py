
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from . import views
urlpatterns = [
	path('staff/staff_info/<int:id>/',views.staff_info,name='info'),
	path('change_info/<int:id>/',views.change_info,name='info'),
    path('',views.index),
    path('staff/',views.staff),
    path('cars/',views.cars)
]
