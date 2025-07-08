from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import TempUser
import random

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        # check if already exists
        if TempUser.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'message': 'Email already used', 'class': 'danger email'})

        otp = str(random.randint(1000, 9999))
        # TempUser.objects.create(name=name, email=email, password=password, otp=otp)
        TempUser.objects.create(name=name, email=email, password=make_password(password), otp=otp)

        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP is {otp}',
            from_email=None,
            recipient_list=[email],
        )

        request.session['email'] = email
        return redirect('otp')

    return render(request, 'register.html')


from django.utils import timezone
from datetime import timedelta

def otp_verify(request):
    email = request.session.get('email')
    if not email:
        return redirect('register')

    temp_user = TempUser.objects.filter(email=email).first()

    if not temp_user:
        return redirect('register')

    # 🔥 Check OTP expiry (10 মিনিট)
    if timezone.now() - temp_user.created_at > timedelta(minutes=10):
        temp_user.delete()
        return render(request, 'register.html', {
            'message': "The OTP has expired. Please register again.",
            'class': 'danger'
        })

    if request.method == "POST":
        otp_input = request.POST.get('otp')

        if temp_user and temp_user.otp == otp_input:
            user = User.objects.create_user(
                username=email.split('@')[0] + str(random.randint(100, 999)),
                email=email,
                password=temp_user.password,
                first_name=temp_user.name
            )
            temp_user.delete()
            return render(request, 'homes.html', {'message': 'OTP Verified. User created!'})

        return render(request, 'otp.html', {'message': 'Invalid OTP', 'class': 'danger', 'email': email})

    return render(request, 'otp.html', {'email': email})



from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'homes.html')


from django.contrib.auth import authenticate, login, logout

def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'message': 'User does not exist', 'class': 'danger email'})

        # Authenticate user
        user_auth = authenticate(request, username=user.username, password=password)

        if user_auth is not None:
            login(request, user_auth)
            return render(request, 'homes.html')
        else:
            return render(request, 'login.html', {'message': 'Invalid password', 'class': 'danger'})

    return render(request, 'login.html')



def logout_user(request):
    logout(request)
    return redirect('login')


# def login(request):
#     return render(request, 'login.html')

# def otp(request):
#     mobile= request.session['mobile']
#     context = {'mobile':mobile}
#     return render(request, 'otp.html')





def home(request):
    data = {'page': 'Home Page',}
    return render(request, 'homes.html', data)

def about(request):
    data={'page':"About Page",}
    return render(request,'abouts.html', data)

def contact(request):
    data= {'page':"Contact Page",}
    return render(request, 'contacts.html',data) 