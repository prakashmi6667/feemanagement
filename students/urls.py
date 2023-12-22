
from django.urls import path, re_path
from students import views, student_view

app_name = 'students'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('add/', views.add, name='registration'),
    path('list/', views.list, name='list'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('status/<int:id>/<int:type>/', views.status, name='status'),
    path('dropout/<int:id>/<int:type>/', views.dropout, name='dropout'),
    path('approve/<int:id>/', views.approve, name='approve'),
    path('student-profile/<int:id>/', views.student_profile, name='student_profile'),
    path('student-profile-st/', views.student_profile_st, name='student_profile_st'),


    path('timetable/add/', views.timetable_add, name='timetable_add'),
    path('timetable/edit/<int:id>/', views.timetable_edit, name='timetable_edit'),
    path('timetable/list/', views.timetable_list, name='timetable_list'),
    path('assignee-timetable/', views.assignee_timetable, name='assignee_timetable'),
    path('student-timetable/', views.student_timetable_list, name='student_timetable_list'),

    path('attendance/add/', views.attendance_add, name='attendance_add'),
    path('attendance/list/', views.attendance_list, name='attendance_list'),
    path('attendance/add/<int:id>/', views.attendanceByTimetable_add, name='attendanceByTimetable_add'),

    path('leave-request/add/', views.Leave_request_add, name='Leave_request_add'),
    path('leave-request/edit/<int:id>/', views.Leave_request_edit, name='Leave_request_edit'),
    path('franchise-rank/list/', views.Leave_request_list, name='Leave_request_list'),
    path('leave-request/status/<int:id>/<int:type>/', views.Leave_request_status, name='Leave_request_status'),

    path('rank/add/', views.rank_add, name='rank_add'),
    path('rank/edit/<int:id>/', views.rank_edit, name='rank_edit'),
    path('rank/list/', views.rank_list, name='rank_list'),
    path('rank/status/<int:id>/<int:type>/', views.rank_status, name='rank_status'),

    path('st/leave-request/add/', student_view.Leave_request_add, name='st_Leave_request_add'),
    path('st/leave-request/edit/<int:id>/', student_view.Leave_request_edit, name='st_Leave_request_edit'),
    path('st/leave-request/list/', student_view.Leave_request_list, name='st_Leave_request_list'),
    path('is_approved/<int:id>', views.is_approved, name='is_approved'),

    
    
    ]
   