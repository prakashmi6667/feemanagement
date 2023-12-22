from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from .models import Student, Timetable, LeaveRequest, Rank, Attendance, AttendanceDetails, TimetableDetails,max_St_Code
from franchises.models import Franchise
from django.core.paginator import Paginator
from .forms import StudentForm, TimetableForm, LeaveRequestForm, RankForm,AssigneeTimetableForm
from django.db.models import F
from franchises.authenticator import Franchise_Session_Not_Required, Franchise_Session_Required
from .authenticator import Student_Session_Not_Required, Student_Session_Required
from datetime import datetime
from courses.models import Course,Duration
from accounts.models import Wallet,WalletStatus,WalletTransaction
from settings.models import PaymentMethod
from django.contrib import messages
from students.models import Student,RankType,Rank,EnquirySource
from fees.models import Fees
# from certificates.models import CertificateRequest
# from exams.models import AdmitCard
# Create your views here.


def max_code(franchise_id):
    obj = Franchise.objects.get(pk=franchise_id)
    if obj:
        st = Student.objects.filter(
            Q(code__isnull=True) | Q(code=''), franchise=obj).count()
        if(st > 0):
            st = Student.objects.filter(
                Q(code__isnull=False), franchise=obj).exclude(Q(code='')).count()
            st += 1
            return obj.code+str(st).zfill(5)


@Franchise_Session_Required
def add(request):
    try:
        __context = {}

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = StudentForm(request.POST, request.FILES)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.code = max_St_Code(frm.franchise.id)
                frm.save()
                try:
                    surcode = EnquirySource.objects.get(name__contains='student')
                    if frm.enquiry_source == surcode:
                        if frm.source_code != '':
                            if Student.objects.filter(code=frm.source_code):
                                
                                objrantype = RankType.objects.get(pk=4)
                                rankpoint = Rank.objects.create(date=datetime.now(),student=frm,
                                                    rank_type=objrantype,points=5,franchise=frm.franchise)
                                rankpoint.save()

                except Exception as error:
                    print(error)
                return redirect(reverse('students:list'))

        else:
            form = StudentForm()

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']
        # print(__context['session'])
        return render(request, 'students/franchise/student-add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def edit(request, id):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(Student, pk=id, franchise__pk=franchise__id)

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = StudentForm(request.POST or None,
                               request.FILES, instance=data)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
                return redirect(reverse('students:list'))

        else:
            form = StudentForm(instance=data)
            print(form.instance.profile_image)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/student-add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def list(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = []
        if request.method == 'GET':
            if 'active' in request.GET:
                def is_active(x): return int(x) == 1

                active = is_active(request.GET['active'])
                print(active, request.GET['active'])

                data = Student.objects.filter(
                    franchise__pk=franchise__id, is_active=active).order_by('-pk')
                __context['query'] = ''
            elif 'query' in request.GET:
                __context['query'] = request.GET['query']
                data = Student.objects.filter(franchise__pk=franchise__id, is_active=True).filter(
                    name__contains=request.GET['query']).order_by('-pk')
            else:
                data = Student.objects.filter(
                    franchise__pk=franchise__id, is_active=True).order_by('-pk')
                __context['query'] = ''
        else:
            data = Student.objects.filter(
                franchise__pk=franchise__id, is_active=True).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # __context['data'] = data
        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/student-list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})

@Franchise_Session_Required
def student_profile(request,id):
    try:   
        __context = {}  

        fr = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
   
             
        objstd = Student.objects.get(pk=id)
        __context['student'] = objstd

        objfee = Fees.objects.filter(student__id = id)
        __context['fee'] = objfee

        # if CertificateRequest.objects.filter(students_id = id).count()>0:
        #     objcertificate = CertificateRequest.objects.get(students_id = id)
        # else:
        #     objcertificate=None
        objcertificate=None
        __context['certificate'] = objcertificate

        return render(request,'students/franchise/student_profile.html',__context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


def student_profile_st(request):
    try:   
        __context = {}  

        # st = Student.objects.get(
        #         pk=request.session['LoggedInStudent']['id'])
   
             
        objstd = Student.objects.get(pk=request.session['LoggedInStudent']['id'])
        __context['student'] = objstd
        print('-=------',objstd)

        objfee = Fees.objects.filter(student__id = objstd.pk)
        __context['fee'] = objfee

        # if CertificateRequest.objects.filter(students__id = objstd.pk).count()>0:
        #     objcertificate = CertificateRequest.objects.get(students__id = objstd.pk)
        # else:
        #     objcertificate=None

        # objcertificate=None   
        # __context['certificate'] = objcertificate

        return render(request,'students/student_profile_st.html',__context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})

@Franchise_Session_Required
def status(request, id, type):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(Student, pk=id, franchise__pk=franchise__id)
        if type == 1:
            data.is_active = True
        else:
            data.is_active = False
        data.save()
        return redirect(reverse('students:list'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def dropout(request, id, type):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(Student, pk=id, franchise__pk=franchise__id)
        if type == 1:
            data.is_drop_out = True
            data.is_active = False
        else:
            data.is_drop_out = False
            data.is_active = True
        data.save()
        return redirect(reverse('students:list'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def approve(request, id):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(Student, pk=id, franchise__pk=franchise__id)
        code = max_code(franchise__id)
        if code:
            data.code = code
            data.email = code+'@utecindia.in'
            data.password = code+'@123'
            data.is_certified = True
            data.save()
        # else:
        #     data.code = ''
        #     data.email = ''
        #     data.password = ''
        #     data.is_certified = False
        #     data.save()

        print('------', code)
        return redirect(reverse('students:list'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def timetable_add(request):
    try:
        __context = {}

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = TimetableForm(request.POST, request.FILES,
                                 request=request, instance=None)

            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
                for qs in form.cleaned_data['days']:
                    frm.days.add(qs)
                frm.save()

                return redirect(reverse('students:timetable_list'))

        else:
            form = TimetableForm(request=request, instance=None)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/timetable-add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})

@Franchise_Session_Required
def assignee_timetable(request):
    try:
        __context = {}

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = AssigneeTimetableForm(request.POST, request.FILES,
                                 request=request, instance=None)

            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
    
                return redirect(reverse('students:assignee_timetable'))

        else:
            form = AssigneeTimetableForm(request=request, instance=None)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/assignee_timetable.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def timetable_edit(request, id):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(Timetable, pk=id, franchise__pk=franchise__id)
        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            initial = {}
            initial['start_time'] = data.start_time
            initial['end_time'] = data.end_time
            initial['days'] = [t.pk for t in data.days.all()]
            initial['is_update'] = True

            form = TimetableForm(request.POST or None, request.FILES,
                                 request=request, instance=data, initial=initial)
            data.delete()
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
                for qs in form.cleaned_data['days']:
                    frm.days.add(qs)
                frm.save()

                return redirect(reverse('students:timetable_list'))

        else:
            initial = {}
            initial['days'] = [
                t.pk for t in data.days.all()]
            initial['start_time'] = data.start_time
            initial['end_time'] = data.end_time
            form = TimetableForm(
                request=request, instance=data, initial=initial)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/timetable-add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def timetable_list(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = []
        if request.method == 'GET':
            if 'query' in request.GET:
                __context['query'] = request.GET['query']
                data = Timetable.objects.filter(
                    franchise__pk=franchise__id, is_active=True).order_by('-pk')
            else:
                data = Timetable.objects.filter(
                    franchise__pk=franchise__id, is_active=True).order_by('-pk')
                __context['query'] = ''
        else:
            data = Timetable.objects.filter(
                franchise__pk=franchise__id, is_active=True).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # __context['data'] = data
        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/timetable-list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def student_timetable_list(request):
    try:
        __context = {}
        objstd = Student.objects.get(pk=request.session['LoggedInStudent']['id'])

        objtimtable  = TimetableDetails.objects.filter(student__id = objstd.id)
        __context['timetable'] = objtimtable

        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/student_timetable_list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})

@Franchise_Session_Required
def attendance_add(request):
    try:
        __context = {}

        timetable = Timetable.objects.values('id', 'start_time', 'end_time').filter(
            franchise__pk=request.session['LoggedInFranchise']['franchise__pk'],
            is_active=True).distinct().order_by('start_time')

        __context['timetable'] = timetable
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/attendance-add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def attendance_list(request):
    try:
        __context = {}

        timetable = Timetable.objects.values('id', 'start_time', 'end_time').filter(
            franchise__pk=request.session['LoggedInFranchise']['franchise__pk'],
            is_active=True).distinct().order_by('start_time')

        if request.GET:
            __date = datetime.strptime(
                request.GET['date'], '%Y-%m-%d')
            __context['month'] = __date.month
            __context['year'] = __date.year

            if request.GET['timetable'] == '0':
               
                attendance = Attendance.objects.filter(date__year=__context['year'],
                                                   date__month=__context['month'])
                student = AttendanceDetails.objects.values('student__pk', 'student__name', 'student__code').filter( attendance__date__year=__context['year'],
                                                                                                               attendance__date__month=__context['month']).distinct()
            else:
                attendance = Attendance.objects.filter(timetable_id=request.GET['timetable'], date__year=__context['year'],
                                                   date__month=__context['month'])

                student = AttendanceDetails.objects.values('student__pk', 'student__name', 'student__code').filter(attendance__timetable_id=request.GET['timetable'], attendance__date__year=__context['year'],
                                                                                                               attendance__date__month=__context['month']).distinct()

            __context['attendance'] = attendance
            __context['student'] = student

            __context['date'] = request.GET['date']
            __context['tt_id'] = request.GET['timetable']

        __context['timetable'] = timetable
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/attendance-list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def attendanceByTimetable_add(request, id):
    try:
        __context = {}
        
        student = Student.objects.filter(
            franchise__pk=request.session['LoggedInFranchise']['franchise__pk'],
            timetabledetails__timetable__pk=id)
            
        
        timetable = Timetable.objects.values('id', 'start_time', 'end_time').filter(
            franchise__pk=request.session['LoggedInFranchise']['franchise__pk'],
            is_active=True).distinct().order_by('start_time')

        if request.method == 'POST':

            lst_Students = request.POST.getlist('student')

            lst_is_present = request.POST.getlist('is_present')
            lst_remarks = request.POST.getlist('remarks')

            date = request.POST['date']
            franchise_id = request.session['LoggedInFranchise']['franchise__pk']

            objCount = Attendance.objects.filter(
                date=date, timetable_id=id, franchise_id=franchise_id).count()

            if objCount <= 0:

                objAtt = Attendance.objects.create(
                    date=date, timetable_id=id, franchise_id=franchise_id)

                row_count = 0
                for index in lst_Students:
                    if len(lst_is_present) > row_count:
                        AttendanceDetails(attendance=objAtt, student_id=index, is_present=lst_is_present[row_count],
                                          remarks=lst_remarks[row_count]).save()
                    row_count += 1
            else:
                objAtt = Attendance.objects.get(
                    date=date, timetable_id=id, franchise_id=franchise_id)

                row_count = 0
                for index in lst_Students:
                    if len(lst_is_present) > row_count:

                        if AttendanceDetails.objects.filter(attendance=objAtt, student_id=index).count() <= 0:
                            AttendanceDetails(attendance=objAtt, student_id=index, is_present=lst_is_present[row_count],
                                              remarks=lst_remarks[row_count]).save()
                        else:
                            objDetails = AttendanceDetails.objects.get(
                                attendance=objAtt, student_id=index)
                            objDetails.is_present = lst_is_present[row_count]
                            objDetails.remarks = lst_remarks[row_count]
                            objDetails.save()

                    row_count += 1

        __context['student'] = student
        __context['timetable'] = timetable
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/attendance-add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def Leave_request_add(request):
    try:
        __context = {}

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = LeaveRequestForm(
                request.POST, request.FILES, request=request)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()

                return redirect(reverse('students:Leave_request_list'))

        else:
            form = LeaveRequestForm(request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']
        # print(__context['session'])
        return render(request, 'students/franchise/Leave_request_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def Leave_request_edit(request, id):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(
            LeaveRequest, pk=id, franchise__pk=franchise__id)

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = LeaveRequestForm(request.POST or None,
                                    request.FILES, instance=data, request=request)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
                return redirect(reverse('students:Leave_request_list'))

        else:
            form = LeaveRequestForm(instance=data, request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/Leave_request_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def Leave_request_list(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = []
        if request.method == 'GET':
            if 'query' in request.GET:
                __context['query'] = request.GET['query']
                data = LeaveRequest.objects.filter(franchise__pk=franchise__id).filter(
                    name__contains=request.GET['query']).order_by('-pk')
            else:
                data = LeaveRequest.objects.filter(
                    franchise__pk=franchise__id).order_by('-pk')
                __context['query'] = ''
        else:
            data = LeaveRequest.objects.filter(
                franchise__pk=franchise__id).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # __context['data'] = data
        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/Leave_request_list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def Leave_request_status(request, id, type):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(
            LeaveRequest, pk=id, franchise__pk=franchise__id)
        data.status = type

        tt = TimetableDetails.objects.get(student=data.student)

        if type == 1:
            objCount = Attendance.objects.filter(
                date=datetime.now(), timetable=tt.timetable, franchise_id=franchise__id).count()

            if objCount <= 0:
                att = Attendance.objects.create(
                    date=datetime.now(), timetable=tt.timetable, franchise_id=franchise__id)
                AttendanceDetails.objects.create(
                    attendance=att, student=data.student, is_present=3, remarks=data.remarks)
            else:
                objAtt = Attendance.objects.get(
                    date=datetime.now(), timetable=tt.timetable, franchise_id=franchise__id)

                if AttendanceDetails.objects.filter(attendance=objAtt, student=data.student).count() <= 0:
                    AttendanceDetails(attendance=objAtt, student=data.student, is_present=3,
                                      remarks=data.remarks).save()
                else:
                    objDetails = AttendanceDetails.objects.get(
                        attendance=objAtt, student=data.student)
                    objDetails.is_present = 3
                    objDetails.remarks = data.remarks
                    objDetails.save()
        else:
            objCount = Attendance.objects.filter(
                date=datetime.now(), timetable=tt.timetable, franchise_id=franchise__id).count()

            if objCount > 0:
                objAtt = Attendance.objects.get(
                    date=datetime.now(), timetable=tt.timetable, franchise_id=franchise__id)

                if AttendanceDetails.objects.filter(attendance=objAtt, student=data.student).count() > 0:
                    AttendanceDetails.objects.get(
                        attendance=objAtt, student=data.student).delete()

        data.save()
        return redirect(reverse('students:Leave_request_list'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def rank_add(request):
    try:
        __context = {}

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = RankForm(
                request.POST, request.FILES, request=request)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()

                return redirect(reverse('students:rank_list'))

        else:
            form = RankForm(request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']
        # print(__context['session'])
        return render(request, 'students/franchise/rank_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def rank_edit(request, id):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(
            Rank, pk=id, franchise__pk=franchise__id)

        if request.method == 'POST':
            franchise = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])
            form = RankForm(request.POST or None,
                            request.FILES, instance=data, request=request)
            if form.is_valid():
                frm = form.save(commit=False)
                frm.franchise = franchise
                frm.save()
                return redirect(reverse('students:rank_list'))

        else:
            form = RankForm(instance=data, request=request)

        __context['form'] = form
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/rank_add.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def rank_list(request):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = []
        if request.method == 'GET':
            if 'query' in request.GET:
                __context['query'] = request.GET['query']
                data = Rank.objects.filter(franchise__pk=franchise__id).filter(
                    name__contains=request.GET['query']).order_by('-pk')
            else:
                data = Rank.objects.filter(
                    franchise__pk=franchise__id).order_by('-pk')
                __context['query'] = ''
        else:
            data = Rank.objects.filter(
                franchise__pk=franchise__id).order_by('-pk')
            __context['query'] = ''

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # __context['data'] = data
        __context['data'] = page_obj
        __context['range'] = paginator.page_range
        __context['session'] = request.session['LoggedInFranchise']

        return render(request, 'students/franchise/rank_list.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Franchise_Session_Required
def rank_status(request, id, type):
    try:
        __context = {}
        franchise__id = request.session['LoggedInFranchise']['franchise__pk']
        data = get_object_or_404(Rank, pk=id, franchise__pk=franchise__id)
        data.status = type
        data.save()
        return redirect(reverse('students:rank_list'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Student_Session_Not_Required
def login(request):
    try:
        __context = {}
        if request.method == 'POST':
            objEmp = Student.objects.values('id', 'name', 'code', 'email', 'franchise', 'franchise__pk').filter(
                email=request.POST['email'], password=request.POST['password'])
            if len(objEmp) > 0:
                request.session['LoggedInStudent'] = objEmp[0]
                return redirect(reverse('students:dashboard'))
            else:
                __context['error'] = 'Invalid email and password!'

        return render(request, 'students/login.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Student_Session_Required
def logout(request):
    try:
        __context = {}
        del request.session['LoggedInStudent']
        return redirect(reverse('students:login'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})


@Student_Session_Required
def dashboard(request):
    try:
        __context = {}
        # views.connection()

        # import pdfkit
        # path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        # pdfkit.from_url("http://google.com", "out.pdf", configuration=config)
    
        objstd = Student.objects.get(pk=request.session['LoggedInStudent']['id'])
        __context['student'] = objstd

        objAtt = AttendanceDetails.objects.filter(student__pk = objstd.id ,is_present =1 ).count()
        __context['att'] = objAtt

        # objfee = Fees.objects.filter(student__pk = objstd.id)

        objrank = Rank.objects.filter(student__pk = objstd.id).count()
        __context['rank'] = objrank

        __context['session'] = request.session['LoggedInStudent']
        return render(request, 'students/dashboard.html', __context)
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})

@Student_Session_Required
def is_approved(request,id):

    try:
        __context = {}
        
        data = Student.objects.get(pk=id)
        if data.is_certified == False:
            data.is_certified = True                                                                                           
        data.save()
       
        objcourse = Course.objects.get(pk=data.course.pk)

        dur = Duration.objects.get(pk=objcourse.duration.pk)

        fr = Franchise.objects.get(
                pk=request.session['LoggedInFranchise']['franchise__pk'])

        wlt = Wallet.objects.get(franchise=fr)
        if wlt.amount>dur.amount:
            wlt.amount = (wlt.amount-dur.amount)
        else:
            messages.add_message(request, messages.ERROR, 'Efficient ballance !')
            if data.is_certified == True:
                data.is_certified = False   
            data.save()
        wlt.save()
        objstatur =  WalletStatus.objects.get(pk=1)
        objpyment = PaymentMethod.objects.get(pk=1)
        date = datetime.now()
        WalletTransaction.objects.create(name=f"Verification Charges {data.code}",amount=dur.amount,date=date,
                                        payment_method=objpyment,payment_id="",order_id="",signature="",status=objstatur,
                                        transaction_type=1,franchise=fr,is_active=True)
        

        
        return redirect(reverse('students:list'))
    except Exception as ex:
        return render(request, 'Franchise_404.html', {'error': ex})

    


