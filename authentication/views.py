from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User
from validate_email_address import validate_email
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import auth_user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.conf import settings
from .utils import generate_token
import threading

class emailThread(threading.Thread):
      def __init__(self,email):
            self.email = email
            threading.Thread.__init__(self)

      def run(self):
            self.email.send()      



@auth_user_should_not_access
def login_user(request):
    if request.method =='POST':
       context = {'data':request.POST}
       username = request.POST.get('username')
       password = request.POST.get('password')

       user = authenticate(request,username=username,password=password)

       if not user.is_email_verified:
             messages.add_message(request,messages.ERROR,
                                  'Email not verfied, please check your email inbox')
             return render(request,'authentication/login.html',context)

       if not user:
             messages.add_message(request,messages.ERROR,
                                  'invalid credintials')
             return render(request,'authentication/login.html',context)
       
       login(request,user)

       messages.add_message(request,messages.SUCCESS,
                                  f'Welcome {user.username}')
       return redirect('home')
    
    return render(request,'authentication/login.html')


      

@auth_user_should_not_access
def register(request):
    if request.method =='POST':
         context = {'has_error':False,'data':request.POST}
         email = request.POST.get('email')
         username = request.POST.get('username')
         password = request.POST.get('password')
         password2 = request.POST.get('password2')

         if len(password)<6:
                messages.add_message(request,messages.ERROR,
                                  'password should be atleast 6 characters')
                context['has_error'] = True

         if password !=password2:
                messages.add_message(request,messages.ERROR,
                                  'password mismatch')
                context['has_error'] = True 
         if not validate_email(email):
                messages.add_message(request,messages.ERROR,
                                  'Enter a valid email address')
                context['has_error'] = True 
         if not username:
                messages.add_message(request,messages.ERROR,
                                  'Username is required')
                context['has_error'] = True  

         if User.objects.filter(username = username).exists(): 
                messages.add_message(request,messages.ERROR,
                                  'Username is taken, choose another one')
                context['has_error'] = True  

                return render(request,'authentication/register.html',context, status=409)

         if User.objects.filter(email = email).exists(): 
                messages.add_message(request,messages.ERROR,
                                  'Email is taken, choose another one')
                context['has_error'] = True 

                return render(request,'authentication/register.html',context, status=409)

         if context['has_error']:
               return render(request,'authentication/register.html',context)

         user = User.objects.create_user(username=username,email=email)
         user.set_password(password)
         user.save() 

         send_activation_email(user,request)

         messages.add_message(request,messages.SUCCESS,
            'We sent you an email to verify your account,please check your inbox')
         return redirect(reverse('login'))               

    return render(request,'authentication/register.html')


def lgoutUser(request):
      logout(request) 

      messages.add_message(request,messages.SUCCESS,
                                  'Logged out succesfully')
      return redirect('login')


generate_token = PasswordResetTokenGenerator()    
def send_activation_email(user,request):
      current_site = get_current_site(request)
      email_subject = 'Activate your account'
      email_body = render_to_string('authentication/activate.html',{
            'user':user,'domain':current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
      })

      email = EmailMessage(subject=email_subject,body=email_body,
                   from_email=settings.EMAIL_FROM_USER,
                   to=[user.email])
      
      if not settings.TESTING:
         emailThread(email).start()

def activate_user(request,udb64,token):
      
      try:
            uid=force_bytes(urlsafe_base64_decode(udb64))
            user = User.objects.get(pk=uid)

      except Exception as e:
            user=None

      if user and generate_token.check_token(user,token):
            user.is_email_verified=True 
            user.save()   

            messages.add_message(request,messages.SUCCESS,
                                  'Email verified, you can now login')
            return redirect(reverse('login')) 
      
      return render(request, 'authentication/activation-failed.html',{'user':user})
  