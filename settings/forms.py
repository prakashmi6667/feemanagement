from django import forms
from .models import District

class OnchangeDistrictbystateForm(forms.ModelForm):
   
    class Meta:
        model = District
        fields = "__all__"
        widgets = {'state':forms.Select(attrs={'onchange':'fn_GetDistrict()'})}