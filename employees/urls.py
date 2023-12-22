
from django.urls import path, re_path
from employees import views

app_name = 'employee'

urlpatterns = [
    path('', views.list, name='list'),
    path('add/', views.add, name='add'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('status/<int:id>/<int:type>/', views.status, name='status'),
    
]
