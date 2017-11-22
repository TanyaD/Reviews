from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from models import *

def index(request): 
    return render(request, 'Loginandregistration/index.html')

def success(request): 


    try:
        request.session['id']
    except KeyError:
        messages.warning(request, "You must be logged in to see the books")
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['id']),
        'lastreviews': Review.objects.all().order_by('-id')[:3],
        'range':range(5),
    }
    #print context
    return render(request, 'Loginandregistration/success.html', context)

def create(request):
    errors=User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error,extra_tags=tag)
        return redirect('/')
    
    hashed = bcrypt.hashpw((request.POST['password'].encode()), bcrypt.gensalt(5))
    query=User.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'], email=request.POST['email'], password=hashed)
    request.session['id']=query.id


    

    return redirect('/success')


def login(request):

    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request,error,extra_tags=tag)
        return redirect('/')

    request.session['id']=User.objects.get(email=request.POST['login_email']).id
    print request.session['id']
    return redirect('/success')

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')


    


