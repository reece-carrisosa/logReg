from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, "logApp/index.html")

def success(request):
    if 'userId' in request.session:
        context = {
            "user": User.objects.get(id=request.session['userId'])
        }
        return render(request, "logApp/success.html", context)
    else:
        messages.add_message(request, messages.ERROR, "Must be a Registered User!!")
        return redirect('/')
def registration(request):

    if request.method == 'POST':
        answer = User.objects.reg(request.POST['firstName'], request.POST['lastName'], request.POST['email'], request.POST['password'], request.POST['passconfirm'])
        if answer['status']:
            # user = answer["data"]
            # messages.add_message(request, messages.SUCCESS, 'Successfully registered (or logged in)!')
            # request.session['firstName'] = request.POST['firstName']
            request.session['userId'] = answer['data'].id
            
            return redirect ("/success")

        else:
            for errors in answer["data"]:
                messages.add_message(request, messages.ERROR, "Registration {}".format(errors))
    return redirect('/')

def login(request):
    # errors = User.objects.login(request.POST['email'], request.POST['password'])
    # if len(errors) == 0:
    #     request.session['firstName'] = User.objects.filter(email=request.POST['email'])[0].firstName

    #     return redirect("/success")
    # else:
    #     messages.add_message(request, messages.ERROR,"Login not valid")
    #     return redirect("/")
    answer = User.objects.login(request.POST['email'], request.POST['password'])
    if answer['status']:
        request.session['userId'] = answer['data'].id
        return redirect('/success')
    else:
        messages.info(request, "Invalid Email or Password")
        return redirect('/')