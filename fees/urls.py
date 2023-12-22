
from django.urls import path, re_path
from fees import views, student_view

app_name = 'fees'

urlpatterns = [
     path('', views.list, name='list'),
     path('add/', views.add, name='add'),
     path('edit/<int:id>/', views.edit, name='edit'),
     path('status/<int:id>/<int:type>/', views.status, name='status'),

     path('installment/add/', views.fee_installment_add,
          name='fee_installment_add'),
     path('installment/edit/<int:id>/',
          views.fee_installment_edit, name='fee_installment_edit'),
     path('installment/status/<int:id>/<int:type>/',
          views.fee_installment_status, name='fee_installment_status'),
     path('installment/', views.fee_installment_list, name='fee_installment_list'),

     path('course/<int:pk>/', views.getcoursebystudentid, name='course'),
     path('course/fee/<int:pk>/', views.getcoursbystudentid, name='course'),
     path('fee-installment/<int:pk>/',
          views.getfeeinstallmentbystudentid, name='fee_installment'),

     path('st/installment/', student_view.fee_installment_list,
          name='st_fee_installment_list'),
     path('st/fee/', student_view.list,
          name='st_fee_list'),
     path('st/fee/add/', student_view.add,
          name='st_fee_add'),
     
     path('recept/print/<int:id>/',views.receipt,
     name='fee_receipt'),
     
     ]
