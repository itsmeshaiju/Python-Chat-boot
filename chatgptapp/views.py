import json
from django.shortcuts import redirect, render
from django.http import HttpResponse,HttpResponseRedirect
import openai
import configparser
import pandas
from django.http import JsonResponse
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.template import loader
from chatgpt.utils import render_to_pdf

config = configparser.ConfigParser()
config.read('config.ini')


# Create your views here.

def index(request):
    return render(request,'index.html')

def generate_content(request):
    if request.method == 'POST':
        try:
            question = request.POST.get('question')

            # Generate an answer from ChatGPT (you can keep this part)
            api_key = "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"  # Replace with your actual API key
            openai.api_key = api_key
            answer_response = openai.Completion.create(
                model="text-davinci-003",
                prompt=question,
                max_tokens=50,
                temperature=0.7,
            )
            answer = answer_response["choices"][0]["text"].strip()

            # Store the question and answer in the database
            user_id = request.session.get('id')
            user = Tbl_User.objects.get(id=user_id)
            question_answer = Tbl_QuestionAnswer(question=question, answer=answer, user=user)
            question_answer.save()

        except Exception as e:
            return render(request, 'index.html', {'error_message': str(e)})
    # Retrieve questions and answers for the current user
    user_id = request.session.get('id')
    question_answers = Tbl_QuestionAnswer.objects.filter(user__id=user_id)
    question_list = Tbl_QuestionAnswer.objects.filter(user_id=user_id).order_by('-timestamp')

    return render(request, 'index.html', {'question_answers': question_answers, 'question_list':question_list,'user_id':user_id})

def download_as_pdf(request):
    ii = request.GET['id']
    var = Tbl_QuestionAnswer.objects.all().filter(user=ii)
    pdf = render_to_pdf('pdf.html', {'var': var})
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=QuestionAnswer.pdf'
    return response

def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Tbl_User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists...')
            return redirect('signup')

        user = Tbl_User(email=email, username=username, password=password)
        user.save()
        messages.success(request, 'Success! Signup Completed...')
        return redirect('login')
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Tbl_User.objects.get(username=username, password=password)
        except Tbl_User.DoesNotExist:
            user = None
        if user is not None:
            request.session['id'] = user.id
            # messages.success(request, 'Login Successfully...')
            return redirect('generate_content')
        else:
            messages.error(request, 'Invalid Credentials...')
            return redirect('login')
    return render(request, 'login.html')


def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        logout(request)
    return HttpResponseRedirect('/')
