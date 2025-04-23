from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name = 'index' ),
    path('login', views.loginPage, name = 'login'),
    path('register', views.registerPage, name = 'register'),
    path('question/<int:id>', views.questionpage, name ='responses'),
    path('newquestion', views.newQuestionPage, name = 'questions'),
    path('logout', views.logoutPage, name = 'logout'),
    path('main', views.main, name = 'main-page' ),
    path('user profile', views.profile, name='profile'),
   
    
    
]