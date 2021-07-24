from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('', views.landingpage, name='index'),
    path('module', views.listviewModule.as_view(), name='module-list'),
    path('module/create', views.createModule.as_view(), name='module-create'),
    path('module/<int:pk>', views.listviewClass.as_view(), name='class-list'),
    path('module/<int:pk>/edit', views.editModule.as_view(), name='module-edit'),
    path('module/<int:pk>/delete',
         views.deleteModule.as_view(), name='module-delete'),
    path('class/create', views.createClass.as_view(), name='class-create'),
    path('class/<int:pk>', views.listviewLesson.as_view(), name='lesson-list'),
    path('class/<int:pk>/edit', views.editClass.as_view(), name='class-edit'),
    path('class/<int:pk>/delete', views.deleteClass.as_view(), name='class-delete'),
    path('lesson/create', views.createLesson.as_view(), name='lesson-create'),
    path('lesson/<int:pk>', views.questionlist, name='question-list'),
    path('lesson/<int:pk>/edit', views.editLesson.as_view(), name='lesson-edit'),
    path('lesson/<int:pk>/delete',
         views.deleteLesson.as_view(), name='lesson-delete'),
    path('new-question', views.newQuestionPage, name='new-question'),
    path('question/<int:id>', views.questionPage, name='question'),
    path('reply', views.replyPage, name='reply'),
    path('question/<int:pk>/delete/',
         views.deleteQuestion.as_view(), name='delete-question'),
    path('question/<int:pk>/edit/',
         views.editQuestion.as_view(), name='edit-question')
]
