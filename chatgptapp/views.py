from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import openai
import configparser
import pandas
from django.http import JsonResponse
from .models import *

config = configparser.ConfigParser()
config.read('config.ini')


# Create your views here.

def index(request):
    return render(request,'index.html')
def list(request):
    queryset=Tbl_QuestionAnswer.objects.all()
    return render(request,'list.html',{'queryset':queryset})






def generate_content(request):
    if request.method == 'POST':
        # Get the user's question from the form
        question = request.POST.get('question')

        # Send the question to ChatGPT for an answer
        try:
            # Configure ChatGPT API key
            # openai.api_key = config['SETTINGS']['API_KEY']
            # openai.api_key = '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'
            openai.api_key ='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'

            # Generate an answer from ChatGPT
            answer_response = openai.Completion.create(
                model="text-davinci-002",
                prompt=question,
                max_tokens=50,  # Adjust the response length as needed
                temperature=0.7,  # Adjust creativity if necessary
            )
            answer = answer_response["choices"][0]["text"].strip()
            print("__________",answer)
            print("__________",question)

            # Store the question and answer in the database
            user=request.session['id']
            user_id=Tbl_User.objects.get(id=user)
            Tbl_QuestionAnswer(question=question,answer=answer,user=user_id).save()

            # return HttpResponse(f"Question: {question}<br>Answer: {answer}")
            # return JsonResponse({'bot_response': answer})
            return HttpResponseRedirect('/generate_content/')
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")

        user = request.session['id']
        dataset=Tbl_QuestionAnswer.objects.all().filter(user=user)
        return render(request, 'index.html',{'dataset':dataset})
    else:
        user = request.session['id']
        dataset = Tbl_QuestionAnswer.objects.all().filter(user=user)
        return render(request, 'index.html', {'dataset': dataset})












# def chat_view(request):
#       if request.method == 'POST':
#         question = request.POST.get('user_message')
#         try:
#             openai.api_key = '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'
#             # Generate an answer from ChatGPT
#             bot_response = openai.Completion.create(
#                 model="text-davinci-002",
#                 prompt=question,
#                 max_tokens=50,  # Adjust the response length as needed
#                 temperature=0.7,  # Adjust creativity if necessary
#             )
#             bot_response_text = bot_response["choices"][0]["text"].strip()
#             print("__________",bot_response_text)
#             print("__________",question)
#
#             # Store the question and answer in the database
#             # Tbl_QuestionAnswer(question=question,answer=bot_response_text).save()
#             chat_log = ChatLog(user_message=question, bot_response=bot_response_text)
#             chat_log.save()
#
#             # return HttpResponse(f"Question: {question}<br>Answer: {bot_response_text}")
#             return JsonResponse({'bot_response': bot_response_text})
#
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {str(e)}")
#
#       return render(request, 'chat.html')


def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        user_exist=Tbl_User.objects.all().filter(email=email)
        if user_exist:
            text="""<script>alert('Email already exist...');window.location='/signup/';</script>"""
            return HttpResponse(text)
        else:
            Tbl_User(email=email,username=username,password=password).save()
            return render(request,'login.html')
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=Tbl_User.objects.all().filter(username=username,password=password)
        if user:
            for x in user:
                request.session['id']=x.id
            return HttpResponseRedirect('/generate_content/')
        else:
            text="""<script>alert('Invalid Credentials...');window.location='/';</script>"""
            return HttpResponse(text)
    else:
        return render(request,'login.html')

def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        logout(request)
    return HttpResponseRedirect('/')