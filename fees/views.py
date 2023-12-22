from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db.models import Q
from django.urls import reverse
from franchises.models import Franchise
from django.core.paginator import Paginator
from django.db.models import F
from franchises.authenticator import Franchise_Session_Not_Required, Franchise_Session_Required

from .models import FeeInstallment, Fees, FeeStatus
from .forms import FeeInstallmentForm, FeesForm
from courses.models import AssignCourse,Course,Duration
from django.core import serializers
from students.models import Student,Other_Facilities,Facilities
import json
# Create your views here.



def getcoursbystudentid(request, pk):
    try:
       

        __crs = Student.objects.get(pk=pk)

        __Data = Course.objects.filter(name=__crs.course)
        # __Duration = Duration.objects.filter(name=__Data[0].duration)
        # __Other_facilities = Other_Facilities.objects.get(student__id=__crs.id)
        # __facilities = Other_Facilities.objects.get(student__id=__crs.id)

        # amount = 0
        # for dt in __Other_facilities:
        #     amount += dt['price']

        qs_json = serializers.serialize('json', __Data)
        # qs_json1 = serializers.serialize('json', __Duration)
        # qs_json2 = serializers.serialize('json', __Other_facilities)
        

        # __context = [
        #     {'Data': qs_json, 'Duration': qs_json1, 'amount': qs_json2}]

        # __context = json.dumps(__context)

        return HttpResponse(qs_json, content_type='application/json')
    except Exception as ex:
        print(ex)
        return HttpResponse(ex, content_type='application/json')

def getcoursebystudentid(request, pk):
    try:
        __crs = Student.objects.get(pk=pk)

        __Data = AssignCourse.objects.filter(
            course=__crs.course, franchise=__crs.franchise)
        qs_json = serializers.serialize('json', __Data)
        return HttpResponse(qs_json, content_type='application/json')
    except Exception as ex:
        print(ex)
        return HttpResponse(ex, content_type='application/json')


def getfeeinstallmentbystudentid(request, pk):
    try:
        __Data = FeeInstallment.objects.filter(student__pk=pk)
        __LastData = Fees.objects.filter(student__pk=pk).order_by('-id')[:1]
        installment = Fees.objects.filter(student__pk=pk).count()
        total_installment = __Data[0].total_installment-installment

        qs_json = serializers.serialize('json', __Data)
        qs_json1 = serializers.serialize('json', __LastData)

        __context = [
            {'Data': qs_json, 'LastData': qs_json1, 'total_installment': str(total_installment)}]

        __context = json.dumps(__context)
        return HttpResponse(__context, content_type='application/json')
    except Exception as ex:
        print(ex)
        return HttpResponse(ex, content_type='application/json')


@Franchise_Session_Required
def fee_installment_add(request):
    try:
        __context = {}

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = FeeInstallmentForm(
                request.POST, request.FILES, request=request, instance=None)

            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                # frm.status = 1
                frm.save()

                return redirect(reverse('fees:fee_installment_list'))

        else:
            form = FeeInstallmentForm(request=request, instance=None)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'fees/franchise/fees_installment_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def fee_installment_list(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = []
        if request.method == 'GET':
            if 'query' in request.GET:
                __context['query'] = request.GET['query']
                data = FeeInstallment.objects.filter(franchise__pk=franchise__id).filter(
                    name__contains=request.GET['query']).order_by('-pk')
            else:
                data = FeeInstallment.objects.filter(
                    franchise__pk=franchise__id).order_by('-pk')
                __context['query'] = ''
        else:
            data = FeeInstallment.objects.filter(
                franchise__pk=franchise__id).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'fees/franchise/fees_installment_list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def fee_installment_edit(request, id):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(
            FeeInstallment, pk=id, franchise__pk=franchise__id)

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = FeeInstallmentForm(request.POST or None,
                                      request.FILES, request=request, instance=data)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
                return redirect(reverse('fees:fee_installment_list'))

        else:
            form = FeeInstallmentForm(request=request, instance=data)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'fees/franchise/fees_installment_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def fee_installment_status(request, id, type):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(
            FeeInstallment, pk=id, franchise__pk=franchise__id)
        if type == 1:
            data.is_active = True
        else:
            data.is_active = False
        data.save()
        return redirect(reverse('fees:fee_installment_list'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def add(request):
    try:
        __context = {}

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = FeesForm(request.POST, request.FILES, request=request)

            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise

                objFee = FeeInstallment.objects.get(student=frm.student)

                if objFee.is_last_installment():
                    sts = FeeStatus.objects.get(pk=2)
                    objFee.status = sts
                    objFee.is_active = False
                    objFee.save()
                frm.save()

                return redirect(reverse('fees:list'))

        else:
            form = FeesForm(request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'fees/franchise/fees_add.html', __context)
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
                data = Fees.objects.filter(franchise__pk=franchise__id).filter(
                    name__contains=request.GET['query']).order_by('-pk')
            else:
                data = Fees.objects.filter(
                    franchise__pk=franchise__id).order_by('-pk')
                __context['query'] = ''
        else:
            data = Fees.objects.filter(
                franchise__pk=franchise__id).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'fees/franchise/fees_list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def edit(request, id):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(
            Fees, pk=id, franchise__pk=franchise__id)

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = FeesForm(request.POST or None,
                            request.FILES, instance=data, request=request)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
                return redirect(reverse('fees:list'))

        else:
            form = FeesForm(instance=data, request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'fees/franchise/fees_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def status(request, id, type):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(
            Fees, pk=id, franchise__pk=franchise__id)
        if type == 1:
            data.is_active = True
        else:
            data.is_active = False
        data.save()
        return redirect(reverse('fees:list'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


def receipt(request,id):
    try:
        __context ={}
        __context['fee']=Fees.objects.get(pk=id)

        return render(request,'fees/fee_receipt.html',__context)

    except Exception as er:

        return render(request,'fees/fee_receipt.html',{'error':er})
