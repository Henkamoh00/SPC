from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from .decorators import user_not_authenticated
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .forms import *
from .models import *
from pages.models import *
from spc import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.db.models.query_utils import Q




# Create your views here.


@login_required(login_url='loginForm')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if profile.status:
        userComments = Comment.objects.filter(status=True, userID=request.user)

        pagination = Paginator(userComments, 5)
        page = request.GET.get('page1')
        try:
            userComments = pagination.page(page)
        except PageNotAnInteger:
            userComments = pagination.page(1)
        except EmptyPage:
            userComments = pagination.page(pagination.num_page)

        return render(request, 'pages/profile.html', 
                    {'title':'الملف الشّخصي', 'profile':profile, 'userComments':userComments, })
    else:
        messages.warning(request, 'ملفّك الشَخصي معطّل اتّصل بالمركز لتفعيله')
        return redirect('index')



@login_required(login_url='loginForm')
def profileUpdate(request):
    profile = Profile.objects.get(user=request.user)
    email = request.user.email
    if request.method == 'POST':
        userUpdateForm = UserUpdateForm(request.POST, instance=request.user)
        profileUpdateForm = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if userUpdateForm.is_valid() and profileUpdateForm.is_valid():
            if userUpdateForm.cleaned_data['email'] != email:
                request.user.is_active = False
                #confirmation email
                current_site = get_current_site(request)
                confirm_subject = "Smart pro centre platform account reconfirmation"
                confirm_message = render_to_string('another/emailConfirmation.html', {
                    'name':request.user.first_name,
                    'domain':current_site.domain,
                    'userId':urlsafe_base64_encode(force_bytes(request.user.pk)),
                    'token':generate_token.make_token(request.user),
                    'protocol':"https" if request.is_secure() else "http",
                })

                conirm_email = EmailMessage(
                    confirm_subject,
                    confirm_message,
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                )

                conirm_email.fail_silently = True
                conirm_email.send()

            userUpdateForm.save()
            profileUpdateForm.save()
            messages.success(request, 'تمّ تعديل الملف بنجاح.')
            return redirect('profile')
    else:
        userUpdateForm = UserUpdateForm(instance=request.user)
        profileUpdateForm = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'forms/profileUpdate.html',
    {'title':'تعديل الملف الشّخصي', 'profile':profile, 'userUpdateForm':userUpdateForm, 'profileUpdateForm':profileUpdateForm})




@login_required(login_url='loginForm')
def passwordChange(request):
    if request.method == 'POST':
        formData = PasswordChangeForm(user=request.user, data=request.POST or None)
        if formData.is_valid():
            if request.user.check_password(str(formData.cleaned_data['old_password'])):
                formData.save()
                messages.success(request, 'تمّ تغيير كلمة المرور بنجاح.')
                return redirect('profileUpdate')
        else:
            messages.error(request, 'فشل تغيير كلمة المرور.')
            for error in list(formData.errors.values()):
                messages.error(request, error)
    else:
        formData = PasswordChangeForm(user=request.user, data=request.POST or None)
    return render(request, 'forms/passwordChange.html', {'title':'تغيير كلمة المرور', 'passwordChange':formData})





def concernsForm(request):
    if request.method == 'POST':
        formData = ConcernsForm(request.POST)
        if formData.is_valid():
            data = formData.save(commit=False)
            data.fullName = request.POST.get('fullname')
            if request.user.is_authenticated:
                data.userID = request.user
            formData.save()
            return redirect('index')
    return render(request, 'forms/concernsForm.html',{'title':'انشغالات المستخدمين', 'concernsForm':ConcernsForm})
    




def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            formData = CustomUserCreationForm(request.POST)
            
            if formData.is_valid():
                user = formData.save()
                messages.success(request, f'تهانينا {user.username} لقد تمّ انشاء الحساب بنجاح.')

                # welcome email
                hi_subject = "مركز سمارت برو يرحب بكم.."
                hi_message = "مرحبا " + user.first_name + " لنا عظيم الشّرف أن انضممت إلى مجتمعنا، نتمنى أن تحضى بتجربة ممتعة في تلقي آخر أخبارنا."
                from_email = settings.EMAIL_HOST_USER
                to_email = [user.email]
                send_mail(hi_subject, hi_message, from_email, to_email, fail_silently=True)

                #confirmation email
                current_site = get_current_site(request)
                confirm_subject = "Smart pro centre platform account confirmation"
                confirm_message = render_to_string('another/emailConfirmation.html', {
                    'name':user.first_name,
                    'domain':current_site.domain,
                    'userId':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':generate_token.make_token(user),
                    'protocol':"https" if request.is_secure() else "http",
                })

                conirm_email = EmailMessage(
                    confirm_subject,
                    confirm_message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )

                conirm_email.fail_silently = True
                conirm_email.send()

                return redirect('loginForm')
                
                
        else:
            formData = CustomUserCreationForm()
            
        return render(request, 'forms/signupForm.html',{'title':'إنشاء حساب', 'signupForm':formData})
        

def createProfile(sender, **kwarg):
    if kwarg['created']:
        Profile.objects.create(user=kwarg['instance'])

post_save.connect(createProfile, sender=User)
        




def login_(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.check_password(password):
                login(request, user)
                messages.success(request, 'تمّ تسجيل الدّخول بنجاح.')
                return redirect('index')
            else:
                messages.error(request, 'اسم المستخدم او كلمة المرور غير صحيح، حاول مجدّداً.')
        return render(request, 'forms/loginForm.html', {'title':'تسجيل الدّخول', 'loginForm':LoginForm})



@login_required(login_url='loginForm')
def logoutAction(request):
    logout(request)
    messages.success(request, 'تمّ تسجيل الخروج بنجاح.')
    return render(request, 'pages/logout.html', {'title':'خروج'} )





def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('loginForm')
    else:
        return render(request, 'another/activationFailed.html')





# @user_not_authenticated
def passwordReset(request):
    if request.method == 'POST':
        formData = PasswordResetForm(request.POST)
        if formData.is_valid():
            email = formData.cleaned_data['email']
            associated_user = User.objects.filter(Q(email=email)).first()
            if associated_user:
                current_site = get_current_site(request)
                subject = "Password Reset"
                message = render_to_string('another/passwordResetEmail.html', {
                    'name':associated_user.first_name,
                    'domain':current_site.domain,
                    'userId':urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token':generate_token.make_token(associated_user),
                    'protocol':"https" if request.is_secure() else "http",
                })

                email = EmailMessage(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [associated_user.email],
                )

                if email.send():
                    messages.success(request, 'تمّ ارسال بريد الكتروني لإعادة تعيين كلمة المرور.')
                else:
                    messages.error(request, 'توجد مشكلة في ارسال بريد الكتروني لإعادة تعيين كلمة المرور.')

            return redirect('loginForm')
    else:
        formData = PasswordResetForm()
    return render(request, 'forms/passwordReset.html', {'title':'استعادة كلمة المرور', 'passwordReset':formData})



def passwordResetConfirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        if request.method == 'POST':
            formData = SetPasswordForm(user, request.POST)
            if formData.is_valid():
                formData.save()
                messages.success(request, 'تمّ تعيين كلمة المرور الجديدة بنجاح.')
                return redirect('loginForm')
            else:
                for error in list(formData.errors.values()):
                    messages.error(request, error)

        formData = SetPasswordForm(user)
        return render(request, 'forms/passwordResetConfirm.html', {'passwordResetConfirm':formData})
    else:
        messages.error(request, 'الرابط منتهي الصلاحيّة.')

    messages.error(request, 'حدث خطأ ما، إعادة التوجيه مرة أخرى إلى صفحة تسجيل الدخول.')
    return redirect('loginForm')