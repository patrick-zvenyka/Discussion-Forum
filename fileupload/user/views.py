from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Response, Subject
from calendar import month_name
from django.db.models import Count
from django.http import HttpResponse
from django.db.models import Count, Q
from datetime import datetime
from django.contrib import messages
from .forms import RegisterUserForm, LoginForm, NewQuestionForm, NewResponseForm, SiteUsersForm
from django.core.paginator import Paginator
from django.shortcuts import render
# Create your views here.

def registerPage(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        try:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, "Account successfully created!")
                login(request, user)
                return redirect('login') 
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form,'title':'StudyCircle | Signup Page'   
    }
    return render(request, 'register.html', context)

def loginPage(request):
    form = LoginForm()
    if request.method == 'POST':
        try:
            form = LoginForm(data = request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('main-page') 
        except Exception as e:
            print(e)
            raise

    context = {'form':form,'title':'StudyCircle | Login Page'}
    return render(request, 'login.html', context)


@login_required(login_url='login.html')
def main(request):
    questions_list = Question.objects.all().order_by('-created_at')

    # Get filter query params
    subject_id = request.GET.get('subject')
    month = request.GET.get('month')
    responses = request.GET.get('responses')

    # Apply Subject Filter
    if subject_id:
        questions_list = questions_list.filter(subject_id=subject_id)

    # Apply Month Filter
    if month:
        questions_list = questions_list.filter(created_at__month=int(month))

    # Apply Response Count Filter
    # if responses:
    #     questions_list = questions_list.annotate(num_responses=Count('responses'))
    #     if responses == "0":
    #         questions_list = questions_list.filter(num_responses=0)
    #     elif responses == "1+":
    #         questions_list = questions_list.filter(num_responses__gte=1)
    #     elif responses == "5+":
    #         questions_list = questions_list.filter(num_responses__gte=5)

    # Pagination
    paginator = Paginator(questions_list, 5)
    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)

    # Context for filters
    subjects = Subject.objects.all()
    months = [{'value': i, 'name': month_name[i]} for i in range(1, 13)]

    context = {
        'questions': questions,
        'title': 'StudyCircle | Dashboard',
        'subjects': subjects,
        'months': months,
    }

    return render(request, 'main.html', context)



def home(request):
   return render (request, 'home.html')

def profile(request):
    user = request.user
    form = SiteUsersForm(instance=user)

    if request.method == 'POST':
        form = SiteUsersForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            
            form.save()
    context ={
        'form': form
    }
    return render(request, 'profile.html', context)

def logoutPage(request):
    logout(request)
    messages.info(request, 'You are logging out!')
    return redirect('login.html')

from django.contrib import messages
from django.shortcuts import redirect

@login_required(login_url='login.html')
def newQuestionPage(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            messages.success(request, 'Your question was posted successfully!')
            return redirect('questions')  # Replace with your actual URL name
    else:
        form = NewQuestionForm()
    
    context = {
        'form': form,
        'title': 'StudyCircle | Ask Questions'
    }
    return render(request, 'questions.html', context)


@login_required(login_url = 'login.html')
def questionpage(request, id):
    response_form = NewResponseForm()

    if request.method == 'POST':
        
        try:
            response_form = NewResponseForm(request.POST, request.FILES)

            if response_form.is_valid():
                pdf = request.FILES.get('pdf')
                response = response_form.save(commit = False)
                response.user = request.user
                response.question = Question(id = id)
                response.save()
                messages.success(request, 'Response submitted!')
                return redirect('/question/'+str(id)+'#'+str(response.id))
            elif response_form.is_valid():
                response = response_form.save(commit = False)
                response.user = request.user
                response.question = Question(id = id)
                response.save()
                messages.success(request, 'Response submitted!')
                return redirect('/question/'+str(id)+'#'+str(response.id))
           
        except Exception as e:
            print(e)
            raise
        


    question = Question.objects.get(id = id)
    context = {
        'question' : question,
        'response_form' : response_form,
        'title':'StudyCircle | Responses'
    }
    return render(request, 'responses.html', context)






