from django import forms
from .models import Employee


class EmployeeInlineForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('name', 'gender', 'job_Type', 'experience',)
        # fields = "__all__"
        # exclude = ('is_approved', 'payment_id', 'order_id', 'signature', 'privacy_policy', 'plan', 'amount')

    def __init__(self, *args, **kw):
        super(EmployeeInlineForm, self).__init__(*args, **kw)


class CenterHeadInlineForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = "__all__"
        exclude = ('religion', 'nationality', 'franchise', 'dob',)

    def __init__(self, *args, **kw):
        super(CenterHeadInlineForm, self).__init__(*args, **kw)
        self.fields['designation'].required = True
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['mobile_no'].required = True
        self.fields['pan_no'].required = True
        self.fields['aadhar_no'].required = True
        self.fields['address'].required = True
        self.fields['state'].required = True
        self.fields['district'].required = True
        self.fields['city'].required = True
        self.fields['pin_code'].required = True


class EmployeeInlineFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(EmployeeInlineFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class CenterHeadInlineFormset(forms.BaseModelFormSet):

    def __init__(self, *args, **kwargs):
        super(CenterHeadInlineFormset, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False



class Employee_WebForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = "__all__"
        exclude = ('franchise',)
        
        widgets = {
            'dob': forms.TextInput(attrs={'type': 'date'}),
            'state': forms.Select(attrs={'onChange': 'fn_GetDistricts()'}),
            'address': forms.Textarea(attrs={'rows':3,}),
        }

    def __init__(self, *args, **kw):
        super(Employee_WebForm, self).__init__(*args, **kw)
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['mobile_no'].required = True
        self.fields['pan_no'].required = True
        self.fields['aadhar_no'].required = True
        self.fields['address'].required = True
        self.fields['state'].required = True
        self.fields['district'].required = True
        self.fields['city'].required = True
        self.fields['post_office'].required = True
        self.fields['police_station'].required = True
        self.fields['pin_code'].required = True
        self.fields['dob'].required = True
        self.fields['designation'].required = True
        self.fields['religion'].required = True
        self.fields['qualification'].required = True
        self.fields['profile_image'].required = True
    
        self.fields['district'].choices = [(0, 'Select District')]
