from django import forms
from .models import FeeInstallment, Fees
from students.models import Student
from django.db.models import F
from courses.models import Course


class FeeInstallmentForm(forms.ModelForm):

    class Meta:
        model = FeeInstallment
        fields = "__all__"
        exclude = ('franchise',)
        widgets = {
            'student': forms.Select(attrs={'onChange': 'fn_GetCourse()'}),
            'course': forms.Select(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        franchise__id = self.request.session['LoggedInFranchise']['franchise__pk']

        super(FeeInstallmentForm, self).__init__(*args, **kw)
        self.fields["student"].queryset = Student.objects.filter(
            is_active=True, franchise__pk=franchise__id).exclude(feeinstallment__student__pk=F('pk'))


class FeesForm(forms.ModelForm):

    class Meta:
        model = Fees
        fields = "__all__"
        exclude = ('franchise', 'payment_id',
                   'order_id', 'signature', 'discount',)

        widgets = {
            
            'student': forms.Select(attrs={'onChange': 'fn_GetCourse()'}),
            'course': forms.Select(attrs={'readonly': 'readonly'}),
            'date': forms.TextInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows':2}),
        }

    field_order = ['student', 'course', 'receipt_no', 'date', 'fee', 'discount', 'fine',
                   'total_amount', 'paid_amount', 'status', 'payment_method',  'payment_reciept', 'remarks']

    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        franchise__id = self.request.session['LoggedInFranchise']['franchise__pk']

        super(FeesForm, self).__init__(*args, **kw)
        self.fields["student"].queryset = Student.objects.filter(
            is_active=True, feeinstallment__student__pk=F('pk'), feeinstallment__status__pk=1)


class Student_FeesForm(forms.ModelForm):

    class Meta:
        model = Fees
        fields = "__all__"
        exclude = ('franchise', 'payment_id', 'receipt_no', 'fine', 'status',
                   'order_id', 'signature', 'discount', 'payment_reciept', 'payment_method',)

        widgets = {
            'student': forms.Select(attrs={'onChange': 'fn_GetCourse()'}),
            'course': forms.Select(attrs={'readonly': 'readonly'}),
            'fee': forms.TextInput(attrs={'readonly': 'readonly'}),
            'total_amount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'paid_amount': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'date': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'date': forms.TextInput(attrs={'type': 'date'}),
        }

    field_order = ['student', 'course', 'date', 'fee',
                   'total_amount', 'paid_amount', 'remarks']

    def __init__(self, *args, **kw):
        self.request = kw.pop("request")
        franchise__id = self.request.session['LoggedInStudent']['franchise__pk']
        student__id = self.request.session['LoggedInStudent']['id']

        super(Student_FeesForm, self).__init__(*args, **kw)
        self.fields["student"].queryset = Student.objects.filter(
            pk=student__id)



class FeeInstallmentForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        widgets = {'student':forms.Select(attrs={'onchange':'fn_GetCourse()'})}