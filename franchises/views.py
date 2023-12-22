from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.urls import reverse
from django.forms import inlineformset_factory
from django.forms import formset_factory, modelformset_factory
from .forms import franchiseForm
from .models import Franchise, MessageBoard,Franchise_Rank
from employees.forms import EmployeeInlineForm, CenterHeadInlineForm, EmployeeInlineFormSet, CenterHeadInlineFormset
from employees.models import Employee
# from websites.forms import ContactUsForm
from .authenticator import Franchise_Session_Not_Required, Franchise_Session_Required
# from migrates import views, SQLQuery
from django.core.paginator import Paginator
from .forms import MessageBoardForm
from students.models import Student,LeaveRequest

from fees.models import Fees,FeeInstallment
from settings.models import District
import os
from django.core import serializers
from django.db.models import Sum
from courses.models import Course
# Create your views here.


def authrization_print(request, pk):
    import datetime
    objData = Franchise.objects.get(pk=pk)
    objEmpData = Employee.objects.get(franchise_id=pk, designation_id=1)
    return render(request, 'franchises/authrization.html', {'data': objData, 'emp': objEmpData, 'date': datetime.date.today()})


@Franchise_Session_Not_Required
def login(request):
    try:
        __context = {}
        # SQLQuery.check_data(request)
        if request.method == 'POST':
            objEmp = Employee.objects.values('id', 'name', 'email', 'franchise', 'franchise__pk').filter(
                email=request.POST['email'], password=request.POST['password'])
            if len(objEmp) > 0:
                request.session['LoggedInFranchise'] = objEmp[0]
                return redirect(reverse('franchises:dashboard'))
            else:
                __context['error'] = 'Invalid email and password!'

        return render(request, 'franchises/franchise/login.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def logout(request):
    try:
        __context = {}
        del request.session['LoggedInFranchise']
        return redirect(reverse('franchises:login'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def dashboard(request):
    try:
        __context = {}
        fr = Franchise.objects.get(
            pk=request.session['LoggedInFranchise']['franchise__pk'])
        student = Student.objects.filter(franchise=fr).count()
        __context['student'] = student

        # certificate = CertificateRequest.objects.filter(is_active=True, franchise=fr,is_sent=True).count()
        # __context['certificatecount'] = certificate
        
        
        student = Student.objects.filter(is_active=True, franchise=fr,).count()
        __context['studentActive'] = student

            
        stApplied = Student.objects.filter(is_active=True, franchise=fr,is_certified=False).count()
        __context['stApplied'] = stApplied

        
        stApprove = Student.objects.filter(is_active=True, franchise=fr,is_certified=True).count()
        __context['stApprove'] = stApprove

        leaveRequest = LeaveRequest.objects.filter(franchise=fr).order_by('-id')[:5]
        __context['leaveRequest'] = leaveRequest

        # certificate = CertificateRequest.objects.filter(franchise=fr).order_by('-id')[:5]
        __context['certificate'] = None

        messagereq = MessageBoard.objects.filter(franchise=fr).order_by('-id')[:5]
        __context['messagereq'] = messagereq

        pendingfee = FeeInstallment.objects.filter(is_active=True,status__name='Pending',franchise=fr).order_by('-id')[:5]
        __context['pendingfee'] = pendingfee

        fee = Fees.objects.filter(franchise=fr).order_by('-id')[:5]
        __context['fee'] = fee

        course = Course.objects.filter(is_active = True).count()
        __context['course'] = course

        FR = Franchise_Rank.objects.filter(franchise=fr).aggregate(total_points=Sum('points'))
        __context['point'] = FR

        # import pdfkit
        # path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        # pdfkit.from_url("http://google.com", "out.pdf", configuration=config)

        __context['session'] = request.session['LoggedInFranchise']
        return render(request, 'franchises/franchise/dashboard.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Not_Required
def registration(request):
    try:
        __context = {}
        if request.method == 'POST':

            # objCenterHeadInlineFormset = formset_factory(
            #     form=CenterHeadInlineForm, max_num=1, extra=1, can_delete=False)
            # objEmployeeInlineFormset = formset_factory(
            #     form=EmployeeInlineForm, max_num=2, extra=2, can_delete=False)

            objCenterHeadInlineFormset = modelformset_factory(Employee,
                                                              form=CenterHeadInlineForm, max_num=1, extra=1, can_delete=False)
            objEmployeeInlineFormset = modelformset_factory(Employee,
                                                            form=EmployeeInlineForm, max_num=2, extra=2, can_delete=False)

            form = franchiseForm(request.POST, request.FILES)
            CenterHeadFormset = objCenterHeadInlineFormset(
                request.POST, request.FILES, prefix='center')
            EmployeeFormset = objEmployeeInlineFormset(
                request.POST, prefix='employee')

            if form.is_valid() and CenterHeadFormset.is_valid():
                franchiseInstance = form.save()

                obj = CenterHeadFormset.save(commit=False)
                for dt in obj:
                    dt.franchise = franchiseInstance
                    dt.save()

                if EmployeeFormset.is_valid():
                    obj = EmployeeFormset.save(commit=False)
                    for dt in obj:
                        dt.franchise = franchiseInstance
                        dt.save()

                # for frm_set in CenterHeadFormset:
                #     dt = frm_set.cleaned_data

                #     Employee(name=dt.get('name'), email=dt.get('email'), password=dt.get('password'), mobile_no=dt.get('mobile_no'),
                #              gender=dt.get('gender'), marital_status=dt.get('marital_status'), job_Type=dt.get('job_Type'),
                #              experience=dt.get('experience'), pan_no=dt.get('pan_no'), aadhar_no=dt.get('aadhar_no'),
                #              address=dt.get('address'), state=dt.get('state'), district=dt.get('district'),
                #              city=dt.get('city'), post_office=dt.get('post_office'), police_station=dt.get('police_station'),
                #              pin_code=dt.get('pin_code'), designation=dt.get('designation'), qualification=dt.get('qualification'),
                #              profile_image=dt.get('profile_image'), franchise=franchiseInstance).save()

                # if EmployeeFormset.is_valid():
                #     for frm_set in CenterHeadFormset:
                #         dt = frm_set.cleaned_data
                #         Employee(name=dt.get('name'), gender=dt.get('gender'), job_Type=dt.get('job_Type'),
                #                  experience=dt.get('experience'), franchise=franchiseInstance).save()

                return redirect(reverse('franchises:successful'))
            else:
                print('Invalid')
        else:

            objCenterHeadInlineFormset = formset_factory(
                form=CenterHeadInlineForm, max_num=1, extra=1, can_delete=False)
            objEmployeeInlineFormset = formset_factory(
                form=EmployeeInlineForm, max_num=2, extra=2, can_delete=False)

            CenterHeadFormset = objCenterHeadInlineFormset(prefix='center')
            EmployeeFormset = objEmployeeInlineFormset(prefix='employee')
            form = franchiseForm()

        __context['form'] = form
        __context['CenterHeadInlineFormset'] = CenterHeadFormset
        __context['EmployeeInlineFormset'] = EmployeeFormset

        return render(request, 'franchises/franchise/registration.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Not_Required
def successful(request, code=''):
    try:
        __context = {}

        # if request.method == 'POST':
        #     form = ContactUsForm(request.POST, request.FILES)

        #     if form.is_valid():
        #         form.save()
        #         __context['success'] = 'We will call back to you soon!'
        #         form = ContactUsForm()
        #     else:
        #         __context['error'] = 'Something went wrong!'
        #         print('Invalid')
        # else:
        #     form = ContactUsForm()

        # __context['form'] = form

        return render(request, 'franchises/franchise/registration-successfull.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def message_board_add(request):
    try:
        __context = {}

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = MessageBoardForm(
                request.POST, request.FILES, request=request)

            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()

                return redirect(reverse('franchises:message_board_list'))

        else:
            form = MessageBoardForm(request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'franchises/franchise/message_board_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def message_board_list(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = []
        if request.method == 'GET':
            if 'query' in request.GET:
                __context['query'] = request.GET['query']
                data = MessageBoard.objects.filter(franchise__pk=franchise__id).filter(
                    name__contains=request.GET['query']).order_by('-pk')
            else:
                data = MessageBoard.objects.filter(
                    franchise__pk=franchise__id).order_by('-pk')
                __context['query'] = ''
        else:
            data = MessageBoard.objects.filter(
                franchise__pk=franchise__id).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'franchises/franchise/message_board_list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def message_board_edit(request, id):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(
            MessageBoard, pk=id, franchise__pk=franchise__id)

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = MessageBoardForm(request.POST or None,
                                    request.FILES, instance=data, request=request)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
                return redirect(reverse('franchises:message_board_list'))

        else:
            form = MessageBoardForm(instance=data, request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'franchises/franchise/message_board_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})



def GetStatebyDistrict(request, pk):
    
    try:
        __Data = District.objects.filter(state__id=pk)

        qu_json = serializers.serialize('json', __Data)
        return HttpResponse(qu_json, content_type='application/json')
    except Exception as er:
        return HttpResponse(er, content_type='application/json')