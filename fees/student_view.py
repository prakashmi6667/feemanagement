from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from .models import Fees, FeeInstallment, FeeStatus, reccipt_code
from settings.models import PaymentMethod
from franchises.models import Franchise
from django.core.paginator import Paginator
from .forms import Student_FeesForm
from django.db.models import F
from students.authenticator import Student_Session_Not_Required, Student_Session_Required
from datetime import datetime
from accounts.models import WalletTransaction,WalletStatus,Wallet
# Create your views here.


@Student_Session_Required
def fee_installment_list(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInStudent']['franchise__pk']
        student_id = request.session['LoggedInStudent']['id']
        data = []
        
        if request.method == 'GET':
            if 'query' in request.GET:
                __context['query'] = request.GET['query']
                data = FeeInstallment.objects.filter(franchise__pk=franchise__id, student__pk=student_id).filter(
                    name__contains=request.GET['query']).order_by('-pk')
            else:
                data = FeeInstallment.objects.filter(
                    franchise__pk=franchise__id, student__pk=student_id).order_by('-pk')
                __context['query'] = ''
        else:
            data = FeeInstallment.objects.filter(
                franchise__pk=franchise__id, student__pk=student_id).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInStudent']

        return render(request, 'fees/students/fees_installment_list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Student_Session_Required
def list(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInStudent']['franchise__pk']
        student_id = request.session['LoggedInStudent']['id']
        data = []
        if request.method == 'GET':
            if 'query' in request.GET:
                __context['query'] = request.GET['query']
                data = Fees.objects.filter(franchise__pk=franchise__id, student__pk=student_id).filter(
                    name__contains=request.GET['query']).order_by('-pk')
            else:
                data = Fees.objects.filter(
                    franchise__pk=franchise__id, student__pk=student_id).order_by('-pk')
                __context['query'] = ''
        else:
            data = Fees.objects.filter(
                franchise__pk=franchise__id, student__pk=student_id).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInStudent']

        return render(request, 'fees/students/fees_list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Student_Session_Required
def add(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInStudent']['franchise__pk']
        student_id = request.session['LoggedInStudent']['id']

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=franchise__id)
            form = Student_FeesForm(
                request.POST, request.FILES, request=request)

            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.receipt_no = reccipt_code()
                sts = FeeStatus.objects.get(pk=1)
                mthd = PaymentMethod.objects.get(pk=1)

                frm.status = sts
                frm.payment_method = mthd
                
                objFee = FeeInstallment.objects.get(student=frm.student)

                if objFee.is_last_installment():
                    sts = FeeStatus.objects.get(pk=1)
                    objFee.status = sts
                    objFee.is_active = False
                    objFee.save()
                frm.save()
                wlsts = WalletStatus.objects.get(pk=3)

                WalletTransaction.objects.create(name=frm.student.name,amount=frm.total_amount,payment_method=mthd,payment_id='gsdhih23lku8u',
                                                order_id='245207',remarks=frm.remarks,status=wlsts,franchise=frm.franchise).save()

                wlt = Wallet.objects.get(pk=frm.franchise.id)
                if wlt:
                   wlt.amount += frm.total_amount
                   wlt.save()



                return redirect(reverse('fees:st_fee_list'))

        else:
            form = Student_FeesForm(request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInStudent']

        return render(request, 'fees/students/fees_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})
