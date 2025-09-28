from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Socialize
from .forms import RegistrationForm
from django.conf import settings
from six import text_type
import time

from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django_forms import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import *
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from .models import UpEvent, Winner, Contributor
from django.utils import timezone
# from django.http import HttpResponse

# Create your views here.
def main(request):
  template = loader.get_template('socialize/main.html')
  return HttpResponse(template.render())
# def upcoming(request):
#   template = loader.get_template('socialize/upcoming.html')
#   return HttpResponse(template.render())
def upcoming(request):
    # Query upcoming events from the database
    events = UpEvent.objects.all()  # Query all UpEvent objects

    # Pass the events queryset to the template
    return render(request, 'socialize/upcoming.html', {'events': events})

def past_events_view(request):
    # Query for past events
    past_events = UpEvent.objects.filter(end_date__lt=timezone.now())

    return render(request, 'socialize/past.html', {'past_events': past_events})
def organize(request):
  template = loader.get_template('socialize/organize.html')
  return HttpResponse(template.render())

def winner(request):
    winners = Winner.objects.all()
    return render(request, 'socialize/winner.html', {'winners': winners})
  
def contact(request):
  template = loader.get_template('socialize/contact.html')
  return HttpResponse(template.render())
def feedback(request):
  template = loader.get_template('socialize/feedback.html')
  return HttpResponse(template.render())

def sign_in(request):
  template = loader.get_template('socialize/sign_in.html')
  return HttpResponse(template.render())

def index(request):
    socialize = Socialize.objects.all()
    return render(request, 'socialize/index.html', {
        #'show_socialize': False,
        # 'show_socialize': True,
        'socialize': socialize
    })
#   return HttpResponse('Hello django!')

def socializes_details(request, socializes_slug):
    # print(socializes_slug)
    try:
      selected_socialize = Socialize.objects.get(slug=socializes_slug)
      if request.method == 'GET':
        # selected_socialize = Socialize.objects.get(slug=socializes_slug)
        registration_form = RegistrationForm()
        # return render(request, 'socialize/socializes-details.html', {
        # 'socialize_found': True,
        # 'socialize': selected_socialize,
        # 'form': registration_form
        #  'form': registration_form
        # 'socialize_title': selected_socialize['title'],
        # Using dot notation in this method
        # 'socialize_title': selected_socialize.title,
        # 'socialize_description': selected_socialize['description']
        # 'socialize_description': selected_socialize.description
    #    })
      else:
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
         # contributor = registration_form.save()
          
           user_email = registration_form.cleaned_data['email_address']
           user_phone = registration_form.cleaned_data['phone_number']
           
           contributor,_ = Contributor.objects.get_or_create(email_address=user_email, phone_number=user_phone)
           selected_socialize.contributor.add(contributor)
           return redirect('registration_complete', socializes_slug=socializes_slug)


      return render(request, 'socialize/socializes-details.html', {
            'socialize_found': True,
            'socialize': selected_socialize,
            'registration_form': registration_form
        })

    except Exception as exc:
        print(exc)
        return render(request, 'socialize/socializes-details.html', {
            'socialize_found': False
        })


def registration_complete(request, socializes_slug):
  socialize = Socialize.objects.get(slug=socializes_slug)
  return render(request, 'socialize/registration-complete.html', {
        'supervisor_email': socialize.supervisor_email
    })  

def register(request):
   if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!")
        
        return redirect('form')
        
   else:    
    return render(request, "socialize/register.html")

    # if request.method == 'POST':
    #     form = registration(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponse("Registration at evento is complete. Now Browse for various events happening around you.")
    # else:
    #     form = registration()

    # return render(request, 'socialize/register.html', {'form': form})


def user_signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('form')

def my_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
          
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "socialize/user.html")
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('form')
    
    return render(request, "socialize/cv-form.html")

#   if request.method == "POST":
#     form = MyForm(request.POST)
#     if form.is_valid():
      
#       form.save()
      
#   else:
#       form = MyForm()
#   return render(request, 'socialize/cv-form.html', {'form2': form})
#    if request.method == 'POST':
#         form = MyForm(request.POST)
    
#         username = request.POST['username']
#         pass1 = request.POST['pass1']
#         user = authenticate(username=username, password=pass1)
        
#         if user is not None:
#             login(request, user)
        
#             # messages.success(request, "Logged In Sucessfully!!")
#             return render(request, "socialize/index.html")
#         else:
#             messages.error(request, "Bad Credentials!!")
#             return redirect('form')
     
#    else:
#       form = MyForm()
#       return redirect('form')
       
def user(request):
    return render(request, "socialize/user.html")
  

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to EVENTO- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to EVENTO!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nNISHCHAL MISHRA"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)

        email_subject = "Confirm your Email @ EVENTO - Django Login!!"

        
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        
            'token': generate_token().make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = False
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "authentication/signup.html")


def activate(request,uidb64,token):
    try:
        # uid = force_text(urlsafe_base64_decode(uidb64))
        uid = urlsafe_base64_decode(uidb64).decode()
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token().check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
        
    else:
        return render(request,'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')
