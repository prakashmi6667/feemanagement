from django import forms
from .models import Student, Timetable, Attendance, LeaveRequest, Rank,TimetableDetails
from django.db.models import F
from django.contrib.admin import widgets
from courses.models import Course
from settings.models import District


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = "__all__"
        exclude = ('is_certified', 'pass_out_date', 'email', 'password', 'franchise',
                   'last_period_date', 'is_drop_out', 'form_code')
        widgets = {
            'join_date': forms.TextInput(attrs={'type': 'date'}),
            'dob': forms.TextInput(attrs={'type': 'date'}),
            'state': forms.Select(attrs={'onChange': 'fn_GetDistricts()'}),
            'address': forms.Textarea(attrs={'rows':3,}),
        }

    field_order = ['name', 'mobile_no', 'course', 'gender', 'marital_status', 'father_name', 'mother_name', 'category', 'religion',
                   'qualification', 'profile_image', 'aadhar_card_image', 'enquiry_source', 'source_code', 'dob', 'join_date',
                   'state', 'district', 'city', 'pin_code']

    def __init__(self, *args, **kw):
        super(StudentForm, self).__init__(*args, **kw)
        self.fields['course'].required = True
        self.fields['gender'].required = True
        self.fields['marital_status'].required = True
        self.fields['religion'].required = True
        self.fields['qualification'].required = True
        self.fields['enquiry_source'].required = True
        self.fields['dob'].required = True
        self.fields['join_date'].required = True
        self.fields['category'].required = True
        self.fields['district'].choices = [(0, 'Select District')]
        if 'instance' in kw:
            objSt = kw['instance']
            self.fields['district'].queryset = District.objects.filter(state=objSt.state)
        else:
            self.fields['district'].choices = [(0, 'Select District')]
        self.fields['course'].label_from_instance = lambda obj: "%s %s [%s]" % (obj.name[:10]+'...', obj.code, obj.duration.name)
        
class TimetableForm(forms.ModelForm):

    class Meta:
        model = Timetable
        fields = "__all__"
        exclude = ('franchise',)
        widgets = {
            'start_time': forms.TextInput(attrs={'type': 'time'}),
            'end_time': forms.TextInput(attrs={'type': 'time'}),
        }

    field_order = ['name', 'course', 'start_time', 'end_time', 'days', ]

    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        self.is_instance = kw.pop("instance")

        super(TimetableForm, self).__init__(*args, **kw)
        # self.fields['course'].queryset=Course.objects.exclude(timetable__course__pk=F('pk'))


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = "__all__"
        exclude = ('franchise',)
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }

    field_order = ['date', 'student', 'is_present', 'remarks']

    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        self.is_instance = kw.pop("instance")

        super(AttendanceForm, self).__init__(*args, **kw)
        # self.fields["start_time"].widget = widgets.AdminTimeWidget()
        self.fields["student"].label_from_instance = lambda obj: "%s (%s)" % (
            obj.name, obj.code)

        # if self.is_instance:
        #     self.fields["student"].queryset = Student.objects.filter(
        #         franchise__pk=self.request.session['LoggedInFranchise']['franchise__pk'],
        #         is_active=True).distinct().order_by('name')
        # else:
        #     self.fields["student"].queryset = Student.objects.filter(
        #         franchise__pk=self.request.session['LoggedInFranchise']['franchise__pk'],
        #         is_active=True).exclude(timetable__student__pk=F('pk')).distinct().order_by('name')

        # from django.db.models import CharField, Value as V
        # from django.db.models.functions import Concat
        # .annotate(name=Concat('name', V(' ( '), 'code', V(') '), output_field=CharField()))


class LeaveRequestForm(forms.ModelForm):

    class Meta:
        model = LeaveRequest
        fields = "__all__"
        exclude = ('franchise',)
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }

    field_order = ['student', 'date', 'status', 'remarks']

    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        franchise__id = self.request.session['LoggedInFranchise']['franchise__pk']

        super(LeaveRequestForm, self).__init__(*args, **kw)
        self.fields["student"].queryset = Student.objects.filter(
            is_active=True, franchise__pk=franchise__id)

        self.fields["student"].label_from_instance = lambda obj: "%s (%s)" % (
            obj.name, obj.code)


class RankForm(forms.ModelForm):

    class Meta:
        model = Rank
        fields = "__all__"
        exclude = ('franchise',)
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }

    field_order = ['student', 'rank_type', 'points', 'date']

    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        franchise__id = self.request.session['LoggedInFranchise']['franchise__pk']

        super(RankForm, self).__init__(*args, **kw)
        self.fields["student"].queryset = Student.objects.filter(
            is_active=True, franchise__pk=franchise__id)

        self.fields["student"].label_from_instance = lambda obj: "%s (%s)" % (
            obj.name, obj.code)


class Student_LeaveRequestForm(forms.ModelForm):

    class Meta:
        model = LeaveRequest
        fields = "__all__"
        exclude = ('franchise', 'student', 'status')
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }

    field_order = ['date', 'remarks']

    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        franchise__id = self.request.session['LoggedInStudent']['franchise__pk']

        super(Student_LeaveRequestForm, self).__init__(*args, **kw)
        # self.fields["student"].queryset = Student.objects.filter(
        #     is_active=True, franchise__pk=franchise__id)

        # self.fields["student"].label_from_instance = lambda obj: "%s (%s)" % (
        #     obj.name, obj.code)


class AssigneeTimetableForm(forms.ModelForm):

    class Meta:
        model = TimetableDetails
        fields = "__all__"
       
    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        franchise__id = self.request.session['LoggedInFranchise']['franchise__pk']

        super(AssigneeTimetableForm, self).__init__(*args, **kw)
        
        self.fields["timetable"].queryset = Timetable.objects.filter(
            is_active=True, franchise__pk=franchise__id)

        self.fields["student"].queryset = Student.objects.filter(
            is_active=True, franchise__pk=franchise__id)