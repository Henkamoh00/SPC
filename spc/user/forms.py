from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.forms.fields import EmailField
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox

# label
# initial
# disabled
# help_text
# widget
# required

# forms.ModelForm --> BaseCreationUserForm --> UserCreationForm --> CustomUserCreationForm

class CustomUserCreationForm(UserCreationForm):# class Meta لي تتم في User لكلاس الحالي وارث لجميع خصائص باقي الكلاسات بما فيهم عملية الربط بالمودل
    username = forms.CharField(required=True, label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم', 'class':'loginInput'}))
    email = forms.EmailField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'البريد الإلكتروني', 'class':'loginInput'}))
    first_name = forms.CharField(required=True, label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'الاسم الأول', 'class':'loginInput'}))
    last_name = forms.CharField(required=True, label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'اسم العائلة', 'class':'loginInput'}))
    password1 = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'كلمة المرور', 'class':'loginInput'}), min_length=8)
    password2 = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'تأكيد كلمة المرور', 'class':'loginInput'}), min_length=8)
    
    class Meta:
        model = User
        # fields = ('__all__')
        fields = ('username', 'email', 'first_name', 
        'last_name', 'password1', 'password2')

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
    #         raise forms.ValidationError('..كلمة المرور غير متطابقة')
    #     return cd['password2']

    # def clean_username(self):
    #     cd = self.cleaned_data
    #     if User.objects.filter(username=cd['username']):
    #         raise forms.ValidationError('..يوجد مستخدم مسجل بهذا الاسم')
    #     return cd['username']

    # def clean_email(self):
    #     cd = self.cleaned_data
    #     if User.objects.filter(email=cd['email']):
    #         raise forms.ValidationError('..يوجد مستخدم مسجل بحساب الايميل هذا')
    #     return cd['email']

    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'].lower(),  
            self.cleaned_data['password1']  
        )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = False
        user.save()
        return user  

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #         if hasattr(self, "save_m2m"):    # هذي تستخدم لما يكون عندي حالة ربط عديد لعديد مع جدول اليوزر
    #             self.save_m2m()
    #     return user





class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(required=True, label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم', 'class':'loginInput'}))
    email = forms.EmailField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'البريد الإلكتروني', 'class':'loginInput'}))
    first_name = forms.CharField(required=True, label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'الاسم الأول', 'class':'loginInput'}))
    last_name = forms.CharField(required=True, label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'اسم العائلة', 'class':'loginInput'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    gend = [('ذكر', 'ذكر'), ('انثى', 'انثى'),]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['gender'].label = ''
        self.fields['gender'].required = True

    image = forms.ImageField(required=True, label='', help_text='', widget=forms.FileInput(attrs={'id':'fileInput', 'class':'imageInput'}))
    phoneNumber = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'رقم الهاتف', 'class':'loginInput'}))
    gender = forms.CharField(required=True, label='', widget=forms.RadioSelect(choices=gend, attrs={'class':'radioInput'}))
    address = forms.CharField(required=True, label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'العنوان', 'class':'loginInput'}))
    class Meta:
        model = Profile
        fields = ['image', 'phoneNumber', 'gender', 'address']





class LoginForm(forms.ModelForm):
    username = forms.CharField(required=True, label='', help_text='', widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم', 'class':'loginInput'}))
    password = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'كلمة المرور', 'class':'loginInput'}), min_length=8)

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            # 'title':forms.TextInput(attrs={'class':'className'}),
        }




class ConcernsForm(forms.ModelForm):
    subject = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'الموضوع', 'class':'loginInput'}))
    fullname = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'الاسم الكامل', 'class':'loginInput'}))
    email = forms.EmailField(   required=True, 
                                label='',
                                widget=forms.TextInput(attrs={'placeholder': 'البريد الإلكتروني، ادخل بريداً إلكترونياً ليتمّ الرد عليك.', 'class':'loginInput'}))
    content = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'ادخل انشغالك كي ننقاشه...', 'class':'commentTextArea consernTextArea'}))
    class Meta:
        model = Concern
        fields = ['subject', 'email', 'fullname', 'content']
        widgets = {
            # 'title':forms.TextInput(attrs={'class':'className'}),
        }




class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'ادخل كلمة المرور القديمة', 'class':'loginInput'}), min_length=8)
    new_password1 = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'تعيين كلمة المرور الجديدة', 'class':'loginInput'}), min_length=8)
    new_password2 = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'تأكيد كلمة المرور الجديدة', 'class':'loginInput'}), min_length=8)

    class Meta:
        model = User
        field_order = ['old_password', 'new_password1', 'new_password2']




class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'البريد الإلكتروني', 'class':'loginInput'}))
    
    class Meta:
        model = User

class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'تعيين كلمة المرور الجديدة', 'class':'loginInput'}), min_length=8)
    new_password2 = forms.CharField(required=True, label='', widget=forms.PasswordInput(attrs={'placeholder': 'تأكيد كلمة المرور الجديدة', 'class':'loginInput'}), min_length=8)

    class Meta:
        model = User
