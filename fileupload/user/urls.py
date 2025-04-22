from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name = 'index' ),
    path('login', views.loginPage, name = 'login.html'),
    path('register', views.registerPage, name = 'register.html'),
    path('question/<int:id>', views.questionpage, name ='responses.html'),
    path('newquestion', views.newQuestionPage, name = 'questions.html'),
    path('logout', views.logoutPage, name = 'logout'),
    path('main', views.main, name = 'main-page' ),
    path('user profile', views.profile, name='profile'),
   
    
    
]