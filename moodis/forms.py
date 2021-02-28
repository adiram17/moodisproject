from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class':'form-control'}))
    message = forms.CharField(label='Message', max_length=1000, widget=forms.Textarea(attrs={'class':'form-control', 'rows'
    :'4'}))

class PatientForm(forms.Form):
    GENDER_CHOICES=[
       ('Male', 'Male'),
       ('Female', 'Female')
    ]
    full_name = forms.CharField(label='Full Name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    age = forms.IntegerField(label='Age', widget=forms.NumberInput(attrs={'class':'form-control'}))

class PatientViewForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'true'}))
    gender = forms.CharField(label='Gender', widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'true'}))
    age = forms.IntegerField(label='Age', widget=forms.NumberInput(attrs={'class':'form-control', 'readonly':'true'}))

class PatientCheckForm(PatientViewForm):
    #TODO add validation no future date, only today and backdate, no duplicate date for same patient
    date = forms.DateField(label='Exam Date (yyyy-mm-dd)', widget=forms.DateInput(attrs={'class':'form-control', 'placeholder':'yyyy-mm-dd'}))

    def clean(self):
        super(PatientCheckForm, self).clean()
        #validation
        return self.cleaned_data

class UserCreationForm(forms.Form):
    GENDER_CHOICES=[
       ('Male', 'Male'),
       ('Female', 'Female')
    ]
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    full_name = forms.CharField(label='Full Name', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class':'form-control'}))
    phone = forms.CharField(label='Phone', max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    age = forms.IntegerField(label='Age', widget=forms.NumberInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    #validation
    def clean(self):
    
        super(UserCreationForm, self).clean()
        useremail = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        user = User.objects.filter(email=useremail)
        if user.exists():
            self._errors['password2'] = self.error_class([
                'Email is already registered'])

        if (password1!=password2):
            self._errors['password2'] = self.error_class([
                'Password confirmation is not match'])

        if (len(password1)<5):
            self._errors['password1'] = self.error_class([
                'Password length min 5 characters'])

        return self.cleaned_data

