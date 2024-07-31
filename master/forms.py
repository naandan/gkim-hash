from django import forms
from import_export.admin import ExportForm
from master.constans import BaptisStatus, Role
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from management.admin import ExportAdminMixin

class DummyForm(forms.ModelForm):
    dummy_field = forms.CharField(max_length=100,required=False)

class FormPassword(UserChangeForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control w-100'}),
        required=False,
        help_text=(
            "<ul> <li> Sandi anda tidak dapat terlalu mirip terhadap informasi pribadi anda. </li>"
            "<li> Kata sandi Anda harus memuat setidaknya 8 karakter. </li>"
            "<li> Sandi anda tidak dapat berupa sandi umum digunakan. </li>"
            "<li> Sandi anda tidak bisa sepenuhnya numerik. </li> </ul>"
            "<li class='text-danger'><b>Perhatian:</b> Sandi di isi jika ingin merubah kata sandi atau membuat akun. </li> </ul>"
        )
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control w-100'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ('password', 'email')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                user = User.objects.get(pk=self.instance.pk) 
                if user.email != email and User.objects.filter(email=email).exists():
                    raise forms.ValidationError("Email ini sudah terdaftar.")
            except User.DoesNotExist:
                if User.objects.filter(email=email).exists():
                    raise forms.ValidationError("Email ini sudah terdaftar.")
            try:
                validate_email(email)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return email

    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.password = make_password(password) 
        else:
            if user.pk:
                existing_user = User.objects.get(pk=user.pk)
                user.password = existing_user.password
        if commit:
            user.save()
        return user

class FormExportRole(ExportAdminMixin):
    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)

        role_name = request.POST.get('role')
        if role_name == "1":
            queryset = queryset.filter(Congregation__is_congregation=True)
        elif role_name == "2":
            queryset = queryset.filter(ServantOfGod__is_servant_of_god=True)
        elif role_name == '3':
            queryset = queryset.filter(Employee__is_employee=True)
        return queryset 

class FormExportBaptism(ExportAdminMixin):
    def get_export_queryset(self, request):
        queryset = super().get_export_queryset(request)

        status = request.POST.get('status') or None
        if status != "0":
            queryset = queryset.filter(status=status)
        return queryset

class BaptismFilterForm(ExportForm):
    status = forms.ChoiceField(label='Status', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        status_choices = list(BaptisStatus.choices)
        status_choices.insert(0, (0, 'All'))
        self.fields['status'].choices = status_choices

class RoleFilterForm(ExportForm):
    role = forms.ChoiceField(label='Role',  required=False,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        status_choices = list(Role.choices)
        status_choices.insert(0, ('', 'All'))
        self.fields['role'].choices = status_choices