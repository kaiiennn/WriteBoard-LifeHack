from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Response, Module, Class, Lessons
from .forms import RegisterUserForm, LoginForm, NewQuestionForm, NewResponseForm, NewReplyForm
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy

# Create your views here.


def registerPage(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        try:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def loginPage(request):
    form = LoginForm()

    if request.method == 'POST':
        try:
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('index')
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'login.html', context)


@login_required(login_url='register')
def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='register')
def newQuestionPage(request):
    form = NewQuestionForm()

    if request.method == 'POST':
        try:
            form = NewQuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
                prikey = form.instance.pk
                return redirect('/question/'+str(prikey))
        except Exception as e:
            print(e)
            raise

    context = {'form': form}
    return render(request, 'new-question.html', context)


def landingpage(request):
    return render(request, "landing-page.html")


def questionPage(request, id):
    response_form = NewResponseForm()
    reply_form = NewReplyForm()

    if request.method == 'POST':
        try:
            response_form = NewResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.question = Question(id=id)
                response.save()
                return redirect('/question/'+str(id)+'#'+str(response.id))
        except Exception as e:
            print(e)
            raise

    question = Question.objects.get(id=id)
    context = {
        'question': question,
        'response_form': response_form,
        'reply_form': reply_form,
    }
    return render(request, 'question.html', context)


@login_required(login_url='register')
def replyPage(request):
    if request.method == 'POST':
        try:
            form = NewReplyForm(request.POST)
            if form.is_valid():
                question_id = request.POST.get('question')
                parent_id = request.POST.get('parent')
                reply = form.save(commit=False)
                reply.user = request.user
                reply.question = Question(id=question_id)
                reply.parent = Response(id=parent_id)
                reply.save()
                return redirect('/question/'+str(question_id)+'#'+str(reply.id))
        except Exception as e:
            print(e)
            raise

    return redirect('index')


class deleteQuestion(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Question
    template_name = "confirm-delete.html"
    success_url = reverse_lazy('index')


class editQuestion(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Question
    template_name = "edit-form.html"
    fields = ['title', 'body']

# Module


class createModule(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Module
    fields = ['module']
    template_name = "createform.html"


class listviewModule(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Module
    template_name = "moduleList.html"


class deleteModule(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Module
    template_name = "confirm-delete.html"
    success_url = reverse_lazy('module-list')


class editModule(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Module
    template_name = "edit-form.html"
    fields = ['module']

# Class


class createClass(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Class
    fields = ['module', 'Class']
    template_name = "createform.html"


class listviewClass(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Class
    template_name = "classList.html"

    def get_queryset(self):
        return Class.objects.filter(module__exact=self.kwargs['pk'])


class deleteClass(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Class
    template_name = "confirm-delete.html"
    success_url = reverse_lazy('module-list')


class editClass(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Class
    template_name = "edit-form.html"
    fields = ['module', 'Class']


# Lessons

class createLesson(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Lessons
    fields = ['Class', 'lessonDateTime', 'lesson']
    template_name = "createform.html"


class listviewLesson(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Lessons
    template_name = "lessonList.html"

    def get_queryset(self):
        return Lessons.objects.filter(Class__exact=self.kwargs['pk'])


class deleteLesson(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = Lessons
    template_name = "confirm-delete.html"
    success_url = reverse_lazy('module-list')


class editLesson(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Lessons
    template_name = "edit-form.html"
    fields = ['Class', 'lessonDateTime', 'lesson']


@login_required(login_url='register')
def questionlist(request, pk):
    questions = Question.objects.filter(
        lesson__exact=pk).order_by('-created_at')
    context = {
        'questions': questions
    }
    return render(request, 'questionlist.html', context)
