# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Count
from .models import *
from .forms import *
import datetime
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'wall/index.html')

def wall(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    context = {
        "form": PostForm(),
        "posts": posts,
        "comments": comments
    }
    return render(request, 'wall/the-wall.html', context)

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)
    if len(user) > 0:
        is_pass = bcrypt.checkpw(password.encode(), user[0].password.encode())
        if is_pass:
            request.session['id'] = user[0].id
            return redirect('/wall')
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
            messages.error(request, error)
        return redirect('/register')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_pw)
        return redirect('/')

def process_post(request):
    title = request.POST['title']
    content = request.POST['content']
    Post.objects.create(title=title, content=content)
    messages.success(request, 'Add Post Successfully')
    return redirect('/wall')

def comment_view(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(posts=post).order_by("-created_at")
    form = CommentForm()
    context = {
        "post": post,
        "form": form,
        "comments": comments
    }
    return render(request, 'wall/comment.html', context)

def process_comment(request, id):
    errors = Comment.objects.validate_comment(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error)
        return redirect('/{}/comment'.format(id))
    else:
        content = request.POST['content']
        users = User.objects.get(id=request.session['id'])
        posts = Post.objects.get(id=id)
        Comment.objects.create(content=content, posts=posts, users=users)
        messages.success(request, 'Comment Successfully Added')
        return redirect('/{}/comment'.format(id))
    

    
    