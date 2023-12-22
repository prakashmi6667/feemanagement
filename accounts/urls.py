
from django.urls import path, re_path
from accounts import views

app_name = 'account'

urlpatterns = [
    path('', views.list, name='list'),
    path('add/', views.add, name='add'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('status/<int:id>/<int:type>/', views.status, name='status'),
    
]
