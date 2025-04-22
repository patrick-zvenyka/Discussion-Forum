from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Question, Response
from django.http import HttpResponse
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
                return redirect('login.html') 
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form,'title':'Signup Page'   
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
                return redirect('main.html') 
        except Exception as e:
            print(e)
            raise

    context = {'form':form,'title':'Login Page'}
    return render(request, 'login.html', context)



@login_required(login_url='login.html')
def main(request):
    questions_list = Question.objects.all().order_by('-created_at')
    paginator = Paginator(questions_list, 5)  # Show 10 per page

    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)

    context = {
        'questions': questions,
        'title': 'MSU Discussion Forum | Dashboard'
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

@login_required(login_url = 'login.html')
def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
        except Exception as e:
            print(e)
            raise
    context = {'form': form, 'title':'MSU Discussion Forum | Ask Questions'
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
        'response_form' : response_form
    }
    return render(request, 'responses.html', context)






