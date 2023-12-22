from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from .models import LeaveRequest, Student
from franchises.models import Franchise
from django.core.paginator import Paginator
from .forms import Student_LeaveRequestForm
from django.db.models import F
from .authenticator import Student_Session_Not_Required, Student_Session_Required
from datetime import datetime
# Create your views here.


@Student_Session_Required
def Leave_request_add(request):
    try:
        __context = {}
    
        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInStudent']['franchise__pk'])
            objStudent = Student.objects.get(
                pk=request.session['LoggedInStudent']['id'])

            form = Student_LeaveRequestForm(
                request.POST, request.FILES, request=request)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.student = objStudent
                frm.status = 0
                frm.save()

                return redirect(reverse('students:st_Leave_request_list'))

        else:
            form = Student_LeaveRequestForm(request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInStudent']
        # print(__context['session'])
        return render(request, 'students/Leave_request_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Student_Session_Required
def Leave_request_edit(request, id):
    try:
        __context = {}
        franchise__id = request.session['LoggedInStudent']['franchise__pk']
        data = get_object_or_404(
            LeaveRequest, pk=id, franchise__pk=franchise__id)

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInStudent']['franchise__pk'])
            form = Student_LeaveRequestForm(request.POST or None,
                                    request.FILES, instance=data, request=request)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
                return redirect(reverse('students:st_Leave_request_list'))

        else:
            form = Student_LeaveRequestForm(instance=data, request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInStudent']

        return render(request, 'students/Leave_request_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Student_Session_Required
def Leave_request_list(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInStudent']['franchise__pk']
        student_id = request.session['LoggedInStudent']['id']
        data = []
        if request.method == 'GET':
            if 'query' in request.GET:
                __context['query'] = request.GET['query']
                data = LeaveRequest.objects.filter(franchise__pk=franchise__id, student__pk=student_id).filter(
                    name__contains=request.GET['query']).order_by('-pk')
            else:
                data = LeaveRequest.objects.filter(
                    franchise__pk=franchise__id, student__pk=student_id).order_by('-pk')
                __context['query'] = ''
        else:
            data = LeaveRequest.objects.filter(
                franchise__pk=franchise__id, student__pk=student_id).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # __context['data'] = data
        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInStudent']

        return render(request, 'students/Leave_request_list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})
