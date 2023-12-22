from django.urls import path, re_path
from settings import views

app_name = 'settings'

urlpatterns = [
    path('districts/<int:pk>/', views.getdistictbystateid, name='Districts'),
    path('plan/<int:pk>/', views.getdetailsbyplan, name='Plan'),
    path('plan/pay/<int:amt>/', views.getOrderID, name='Planpay'),
    path('district/<int:id>/',views.getdistictbystateid, name ="getdistictbystateid"),

]
