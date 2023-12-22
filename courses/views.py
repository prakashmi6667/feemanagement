from django.shortcuts import render
from .models import Course, AssignCourse
from franchises.authenticator import Franchise_Session_Not_Required, Franchise_Session_Required
from .forms import AssignCourseForm,CourseForm
from django.db.models import Q
# Create your views here.


@Franchise_Session_Required
def Assign_course_list(request):
    try:
        __context = {}
        data = None
        form = None
        if request.method == 'POST':
            print(request.POST)
            try:
                data = AssignCourse.objects.get(
                    franchise__pk=request.POST['franchise'], course__pk=request.POST['course'])
                print(data)

            except Exception as ex:
                print(ex)
                data = None
                # form = AssignCourseForm(
                #     request.POST, request.FILES, request=request)
            if data:
                form = AssignCourseForm(
                    request.POST, request.FILES, request=request, instance=data)
            else:
                form = AssignCourseForm(
                    request.POST, request.FILES, request=request)

            if form.is_valid():
                form.save()
        query = ''
        if request.method == 'GET':
            if 'query' in request.GET:
                objCourse = Course.objects.filter(is_active=True).filter(
                    Q(code__contains=request.GET['query']) | Q(name__contains=request.GET['query']) |
                    Q(duration__name__contains=request.GET['query']))
                query = request.GET['query']
            else:
                objCourse = Course.objects.filter(is_active=True)
        else:
            objCourse = Course.objects.filter(is_active=True)

        __context['query'] = query
        __context['data'] = objCourse
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'courses/franchise/assign_course.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})



@Franchise_Session_Required
def course_report(request):
    try:
        __context = {}
        data = None
        form = None
        if request.method == 'POST':
            print(request.POST)
            try:
                data = AssignCourse.objects.get(
                    franchise__pk=request.POST['franchise'], course__pk=request.POST['course'])
                print(data)

            except Exception as ex:
                print(ex)
                data = None
                # form = AssignCourseForm(
                #     request.POST, request.FILES, request=request)
            if data:
                form = CourseForm(
                    request.POST, request.FILES, request=request, instance=data)
            else:
                form = CourseForm(
                    request.POST, request.FILES, request=request)

            if form.is_valid():
                form.save()
        query = ''
        if request.method == 'GET':
            if 'query' in request.GET:
                objCourse = Course.objects.filter(is_active=True).filter(
                    Q(code__contains=request.GET['query'].strip()) | Q(name__contains=request.GET['query'].strip()) |
                    Q(duration__name__contains=request.GET['query'].strip()))
                query = request.GET['query']
            else:
                objCourse = Course.objects.filter(is_active=True)
        else:
            objCourse = Course.objects.filter(is_active=True)

        __context['query'] = query
        __context['data'] = objCourse
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'courses/franchise/course_report.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})
