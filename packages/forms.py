from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Package, Image, Booking, Feedback
from .widgets import MultipleFileInput
from django.forms import modelformset_factory
import datetime

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['package', 'feedback_text']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'package': forms.Select(attrs={'class': 'form-control'}),

        }

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'overview', 'cost','number_of_days']

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Package Name'})
    )

    cost = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cost...'})
    )

    overview = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your words here...'})
    )

   

    number_of_days = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter of number of days...'})
    )

class BookingForm(forms.ModelForm):
    

    user = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = Booking
        fields = ['package', 'booking_date', 'status', 'start_date']

        STATUS_CHOICES = (
            ('complete', 'Complete'),
            ('pending', 'Pending'),
            ('cancelled', 'Cancelled'),
        )

        widgets = {
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'package': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=STATUS_CHOICES, attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user_instance:
            self.fields['user'].initial = user_instance.username
            self.fields['user'].widget.attrs['value'] = user_instance.username

        # Set initial value for booking_date to today's date
        self.fields['booking_date'].initial = datetime.date.today().strftime('%Y-%m-%d')


    

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-user',
            'aria-describedby': 'emailHelp', 
            'placeholder': 'Enter your username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter Your Email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter Your password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Confirm Your password'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match")

        return cleaned_data
    

     
 