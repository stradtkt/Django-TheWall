# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'wall/index.html')

def wall(request):
    return render(request, 'wall/the-wall.html')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)
    if len(user) > 0:
        is_pass = bcrypt.checkpw(password.encode(), user[0].password.encode())
        if is_pass:
            request.session['id'] = user[0].id
            return redirect('/')
        else:
            messages.error(request, "Incorrect email and/or password")
            return redirect('/login')
    else:
        messages.error(request, "User does not exist")
    return redirect('/login')

def register(request):
    errors = User.objects.validate_user(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/register')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_pw)
        user = User.objects.get(email=email)
        request.session['id'] = user.id
        return redirect('/')