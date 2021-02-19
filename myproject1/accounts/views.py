from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.

def register(request):
    if request.method == 'POST': # if request is POST then fetch all the values coming from the user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2: # checking if password and confirm password matches
            if User.objects.filter(username = username).exists(): # if this returns true it means that this username is already taken
                messages.info(request, 'Username already taken')
                return render(request, 'register.html')
            elif User.objects.filter(email = email).exists(): # if this returns true it means email is already taken / used
                messages.info(request, 'Email is already registered')
                return render(request, 'register.html')
            else:
                # here we create a user object and only pass one password as in auth_user table we don't have confirm_password field
                user = User.objects.create_user(username = username, password = password1, email = email, first_name = first_name, last_name = last_name)
                # now we got the object so will save it
                user.save();
                print('user created') # to print on terminal when user is saved to database
                return render(request, 'login.html') # and then redirect to login page
        else:
            messages.info(request, 'password not matching...')
            return render(request, 'register.html')
        
    else: # else call registeration page
        return render(request,'register.html')

def login(request):
    if request.method == 'POST': # if request is POST then fetch the data 
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            print('user logged in successfully')
            return redirect('index')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'login.html')

    else: # else call login page
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    print('user logged out successfully')
    return redirect('index')
