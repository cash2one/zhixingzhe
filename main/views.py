#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from blog.models import UserProfile, Answer, Topic, Question, Vote
from blog.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, VoteForm, AvatarForm, DescForm, PostAdminForm



def home(request):
    context = {}
    if request.user.is_anonymous():
        context['user_id']=-1
    else:
        context['user_id']=request.user.id
    return render(request, "home.html",context)

def detail(request, question_id):
    context = {}
    form = PostAdminForm()
    if request.user.is_anonymous():
        context['user_id']=-1
    else:
        context['user_id']=request.user.id
    context['question_id']=question_id
    context['form']=form
    return render(request, "detail.html", context)


def answer(request):
    context = {}
    if request.method == 'GET':
        topics=Topic.objects.all()
        for topic in topics:
            if topic.question_set.all().count()==0:
                topic.delete()
        if request.user.is_anonymous():
            context['user_id']=-1
        else:
            context['user_id']=request.user.id
    return render(request, "answer.html", context)


@login_required
def profile(request,user_id):
    context = {}
    if request.method == 'GET':
        aform=AvatarForm()
        user=User.objects.get(id=user_id)
        answers = Answer.objects.filter(author_id=user_id)
        questions = Question.objects.filter(author_id=user_id)
        profile =UserProfile.objects.get(belong_to=user)
        context["answers"] = answers
        context["questions"] = questions
        context["profile"] = profile
        context["aform"] = aform
        context['user_id'] = user_id
    if request.method == 'POST':
        if request.POST.get('desc'):
            p = UserProfile.objects.get(belong_to=request.user)
            p.desc=request.POST.get('desc')
            p.save()
        else:
            af = AvatarForm(request.POST, request.FILES)
            if af.is_valid():
                avatar = af.cleaned_data['avatar']
                p=UserProfile.objects.get(belong_to=request.user)
                p.avatar.delete()
                p.avatar = avatar
                p.save()
        return  redirect(to="profile",user_id=request.user.id)
    return render(request, "profile.html", context)




def index_login(request):
    context = {}
    if request.method == 'GET':
        form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                username = User.objects.get(email=email).username
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return redirect(to="home")
                else:
                    raise Exception('password or email is not correct')
            except:
                form = LoginForm()
                form.errors['注意:'] = (u"请输入正确的邮箱和密码")
    context['form'] = form
    return render(request, "login.html", context)

@login_required
def index_logout(request):
    logout(request)
    return redirect(to='home')

def register(request):
    context = {}
    if request.method == 'GET':
        form = RegisterForm()
        context['form'] = form
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['name']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username) or User.objects.filter(email=email):
                form = RegisterForm()
                form.errors['注意:'] = (u"用户已存在，请更换用户名或邮箱注册")
            else:
                user = User()
                user.username = username
                user.email = email
                user.set_password(form.cleaned_data['password'])
                user.save()
                p=UserProfile(belong_to=user)
                p.name=username
                p.email=email
                p.save()
                return redirect(to='login')
        context['form'] = form
    return render(request, "register.html", context)

@login_required(redirect_field_name='login')
def search(request):
    context = {}
    q = request.GET.get("q", "").strip()
    if not q:
        return redirect(to="home")

    context["q"] = q

    answers = Answer.objects.filter(content__contains=q)

    context["answers"] = answers
    if request.user.is_anonymous():
        context['user_id']=-1
    else:
        context['user_id']=request.user.id
    return render(request, "search.html", context)
