
from django.urls import path, re_path
from courses import views

app_name = 'courses'

urlpatterns = [
    path('assign-course/', views.Assign_course_list, name='Assign_course_list'),
    path('course-report/', views.course_report, name='course_report'),
]
