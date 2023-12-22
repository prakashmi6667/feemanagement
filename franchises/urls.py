
from django.urls import path, re_path
from franchises import views

app_name = 'franchises'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('successful/', views.successful, name='successful'),
    path('print/<int:pk>/', views.authrization_print, name='authrization_print'),
     
    path('message-board/add/', views.message_board_add, name='message_board_add'),
    path('message-board/edit/<int:id>/', views.message_board_edit, name='message_board_edit'),
    path('message-board/', views.message_board_list, name='message_board_list'),
    path('district/<int:pk>/',views.GetStatebyDistrict,
        name='GetStatebyDistrict'),
]
