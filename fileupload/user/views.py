from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from calendar import month_name
from django.db.models import Count
from django.http import HttpResponse
from django.db.models import Count, Q
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from calendar import month_name
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
    total_questions = questions_list.prefetch_related('responses').count()
    user_questions = Question.objects.filter(author=request.user).count()
    total_responses = Response.objects.count()

    # Get filter query params
    subjects_total = Subject.objects.all().count()
    subject_id = request.GET.get('subject')
    month = request.GET.get('month')
    responses = request.GET.get('responses')

    # Apply Subject Filter
    if subject_id:
        questions_list = questions_list.filter(subject_id=subject_id)

    # Apply Month Filter
    if month:
        questions_list = questions_list.filter(created_at__month=int(month))

    # Pagination
    paginator = Paginator(questions_list, 5)
    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)

    # Subjects with question counts
    subjects = Subject.objects.annotate(total_questions=Count('question'))

    # Months with question counts
    months_query = Question.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(total_questions=Count('id')).order_by('month')
    months = []
    for m in months_query:
        if m['month']:  # in case month is null
            months.append({
                'value': m['month'],
                'name': month_name[m['month']],  # Full month name
                'total_questions': m['total_questions']
            })

    context = {
        'questions': questions,
        'title': 'StudyCircle | Dashboard',
        'subjects': subjects,
        'months': months,
        'total_questions': total_questions,
        'total_responses': total_responses,
        'user_questions': user_questions,
        'subjects_total': subjects_total
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
        'form': form,
        'title': 'StudyCirle | Profile'
    }
    return render(request, 'profile.html', context)

def logoutPage(request):
    logout(request)
    messages.info(request, 'You are logging out!')
    return redirect('login')


@login_required(login_url='login.html')
def newQuestionPage(request):
    if request.method == 'POST':
        form = NewQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
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






