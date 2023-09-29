import openai
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
import config
from chatgpt.utils import render_to_pdf
from .models import *


@login_required
def generate_content(request):
    if request.method == 'POST':
        try:
            question = request.POST.get('question')
            # Generate an answer from ChatGPT
            api_key = config.Api_key
            openai.api_key = api_key

            answer_response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=question,
                max_tokens=2000,
                temperature=0.7,
                stop=None,
            )

            answer = answer_response["choices"][0]["text"].strip()

            # Store the question and answer in the database
            user = User.objects.get(id=request.user.id)  # Assuming request.user is a User instance
            question_answer = QuestionAnswer(question=question, answer=answer, user=user)
            question_answer.save()

            # Redirect to a success page or the same page
            return redirect('/')

        except Exception as e:
            return render(request, 'index.html', {'error_message': str(e)})

    # Retrieve questions and answers for the current user
    user_id = request.user.id
    question_answers = QuestionAnswer.objects.filter(user=user_id)
    question_list = QuestionAnswer.objects.filter(user=user_id).order_by('-timestamp')
    paginator = Paginator(question_list, 8)
    page_number = request.GET.get("page")
    question_list = paginator.get_page(page_number)
    user_data = request.user

    return render(request, 'index.html', {
        'question_answers': question_answers,
        'question_list': question_list,
        'user': user_data
    })

def download_as_pdf(request):
    user_id = request.user.id
    if request.user.is_authenticated:
        var = QuestionAnswer.objects.all().filter(user=user_id)
        user = request.user  # Get the user object

        if user:
            # Create a filename with the username
            filename = f"{user.username}.pdf"
            pdf = render_to_pdf('pdf.html', {'var': var, 'user': user})

            # Set the Content-Disposition header with the dynamic filename
            response = HttpResponse(pdf, content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            # Handle the case when the user is not found
            return HttpResponse("User not found", status=404)
    else:
        # Handle the case when the user is not authenticated
        return HttpResponse("User not authenticated", status=401)
#delete question list
@login_required
def delete_question(request, question_id):
    try:
        question = QuestionAnswer.objects.get(id=question_id)
        question.delete()
    except QuestionAnswer.DoesNotExist:
        pass
    return redirect('/')