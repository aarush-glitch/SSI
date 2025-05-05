from django import forms
from Nurse.forms import DEPARTMENT_CHOICES

class SrDoctorForm(forms.Form):
    name = forms.CharField(max_length=100, label="Employee Name", required=True)
    email = forms.EmailField(max_length=100, label="Employee Name", required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], label="Employee Name", required=True)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, label="Employee Department", required=True)
    phone_number = forms.CharField(max_length=10, required=True, label="Phone Number")
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")

class SrDoctorUpdateForm(forms.Form):
    name = forms.CharField(max_length=100, label="Employee Name", required=True)
    email = forms.EmailField(max_length=100, label="Employee Name", required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], label="Employee Name", required=True)
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES, label="Employee Department", required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label="Date of Birth")
