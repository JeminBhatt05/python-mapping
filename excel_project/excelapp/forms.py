from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
import re
class UploadFileForm(forms.Form):
    file = forms.FileField()

class RegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField(label="Email")
    mobile = forms.CharField(max_length=10,min_length=10)
    password = forms.CharField(widget=forms.PasswordInput,min_length=8,)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class CustomPasswordValidator:
        def validate(self, password):
            if not re.match(r'[A-Z]', password):
                raise ValidationError(
                    _("Your password must contain at least one uppercase letter."),
                    code='password_no_uppercase',
                )
            if not re.search(r'[a-z]', password):
                raise ValidationError(
                    _("Your password must contain at least one lowercase letter."),
                    code='password_no_lowercase',
                )
            if not re.search(r'[0-9]', password):
                raise ValidationError(
                    _("Your password must contain at least one digit."),
                    code='password_no_digit',
                )
            if not re.search(r'[^A-Za-z0-9]', password): # Matches any non-alphanumeric character
                raise ValidationError(
                    _("Your password must contain at least one special character (e.g., !, @, #, $)."),
                    code='password_no_special',
                )

        def get_help_text(self):
            return _(
                "Your password must contain at least one uppercase letter, "
                "one lowercase letter, one digit, and one special character."
            )
    class Meta:
        model = User
        fields = ['name', 'email', 'mobile', 'password', 'confirm_password']

    def clean_phone_number(self):
        mobile = self.cleaned_data['mobile']
        if len(mobile) > 10:
            raise forms.ValidationError("Phone number cannot exceed 10 digits.")
        if len(mobile) < 10:
            raise forms.ValidationError("Phone number cannot less than 10 digits.")
        if not re.match(r'^\d{10}$', mobile): # Optional: ensure exactly 10 digits and only numbers
            raise forms.ValidationError("Please enter a valid 10-digit phone number.")
        return mobile
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")
    
    
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Mobile Number",max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)
    
    
import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


class UploadFileForm(forms.Form):
    file = forms.FileField()


# ✅ Custom password validator (moved outside for reuse)
class CustomPasswordValidator:
    def validate(self, password):
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password must contain at least one uppercase letter."))
        if not re.search(r'[a-z]', password):
            raise ValidationError(_("Password must contain at least one lowercase letter."))
        if not re.search(r'[0-9]', password):
            raise ValidationError(_("Password must contain at least one digit."))
        if not re.search(r'[^A-Za-z0-9]', password):
            raise ValidationError(_("Password must contain at least one special character (!, @, #, etc.)."))

    def get_help_text(self):
        return _(
            "Your password must contain at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character."
        )


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField(label="Email")
    mobile = forms.CharField(max_length=10, min_length=10)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile', 'password', 'confirm_password']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\d{10}$', mobile):
            raise forms.ValidationError("Please enter a valid 10-digit phone number.")
        return mobile

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validator = CustomPasswordValidator()
        validator.validate(password)  # ✅ Perform the validation
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Mobile Number", max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)
