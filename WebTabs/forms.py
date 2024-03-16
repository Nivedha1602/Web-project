# from django import forms
# from .models import User

# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'project_name', 'password']           // basic  understanding code 
#         widgets = {'password': forms.PasswordInput()}






from django import forms
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User

def password_validator(value):
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('Password must contain at least one digit.'), code='password_no_digit')
    if not any(char.islower() for char in value):
        raise ValidationError(_('Password must contain at least one lowercase letter.'), code='password_no_lowercase')
    if not any(char.isupper() for char in value):
        raise ValidationError(_('Password must contain at least one uppercase letter.'), code='password_no_uppercase')
    if not any(char.isalnum() for char in value):
        raise ValidationError(_('Password must contain at least one non-alphanumeric character.'), code='password_no_special_char')
    if len(value) < 8:
        raise ValidationError(_('Password must be at least 8 characters long.'), code='password_too_short')
    if len(value) > 20:
        raise ValidationError(_('Password must be at most 20 characters long.'), code='password_too_long')

class SignupForm(forms.ModelForm):
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(),
        validators=[
            MinLengthValidator(8),
            MaxLengthValidator(20),
            password_validator,
        ],
        help_text=_(
            "Your password must contain at least 8 characters, including "
            "at least one digit, one uppercase letter, one lowercase letter, "
            "and one non-alphanumeric character."
        ),
    )
    confirm_password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(),
        label='Confirm Password'
    )
    #project_name = forms.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['name', 'project_name', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError(
                _("The two password fields didn't match."),
                code='password_mismatch'
            )

        return cleaned_data
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'name@projectname'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())