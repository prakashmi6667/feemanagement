from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from franchises.models import Franchise
from django.core.paginator import Paginator
from franchises.authenticator import Franchise_Session_Not_Required, Franchise_Session_Required

from .models import Employee
from .forms import Employee_WebForm

# Create your views here.


@Franchise_Session_Required
def add(request):
    try:
        __context = {}

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = Employee_WebForm(request.POST, request.FILES)

            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()

                return redirect(reverse('employee:list'))

        else:
            form = Employee_WebForm()

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'employees/franchise/employee_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def list(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = []
        if request.method == 'GET':
            if 'query' in request.GET:
                __context['query'] = request.GET['query']
                data = Employee.objects.filter(franchise__pk=franchise__id).filter(
                    name__contains=request.GET['query']).order_by('-pk')
            else:
                data = Employee.objects.filter(
                    franchise__pk=franchise__id).order_by('-pk')
                __context['query'] = ''
        else:
            data = Employee.objects.filter(
                franchise__pk=franchise__id).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'employees/franchise/employee_list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def edit(request, id):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(
            Employee, pk=id, franchise__pk=franchise__id)

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = Employee_WebForm(request.POST or None,
                                      request.FILES, instance=data)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
                return redirect(reverse('employee:list'))

        else:
            form = Employee_WebForm(instance=data)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'employees/franchise/employee_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})

@Franchise_Session_Required
def status(request, id, type):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(
            Employee, pk=id, franchise__pk=franchise__id)
        if type == 1:
            data.is_active = True
        else:
            data.is_active = False
        data.save()
        return redirect(reverse('employee:list'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


