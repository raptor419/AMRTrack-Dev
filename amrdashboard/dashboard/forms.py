from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import PathTest
from bootstrap_datepicker_plus import DatePickerInput


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class PathTestForm(forms.ModelForm):
    class Meta:
        model = PathTest
        fields = ('testid', 'date', 'year', 'month', 'week', 'sampletype', 'collsite')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))


class InputDataForm(forms.Form):
    keywords = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Keywords'}),required=False)
    ams = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Select Antimicrobial", required=False)
    site = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Select Collection Location", required=False)
    org = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Select Organisms", required=False)
    col = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Select Collection Type", required=False)
    startdate = forms.DateField(label='Enter end Date', widget=DatePickerInput, required=False)
    enddate = forms.DateField(label='Enter Start Date', widget=DatePickerInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))
