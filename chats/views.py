from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Q

from .models import Question, Comment
from .forms import QuestionForm, CommentForm


def index(request):
    questions = Question.objects.all()
    comments = Comment.objects.filter()
    return render(request, 'chats/index.html', context={'questions': questions, 'comments': comments})


@login_required(login_url='/quests')
def question_add(request, question_p_id=None):
    question_p =  None

    if question_p_id:
        question_p = Question.objects.get(id=question_p_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            new_question = form.save(commit=False)
            new_question.user = request.user
            new_question.question_p = question_p
            new_question.save()
            return redirect('index')
    else:
        form = QuestionForm()

    comments = Comment.objects.filter(question=question_p) if question_p else None

    return render(request, 'chats/add_question.html', context={'form': form, 'question_p': question_p, 'comments': comments})


@login_required(login_url='/quests')
def comment_add(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    comments = Comment.objects.filter(question=question)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.question = question
            new_comment.save()

            question.comment_count = comments.count()
            question.save()

            return redirect('index')
    else:
        form = CommentForm()

    return render(request, 'chats/add_comment.html', {'question': question, 'comments': comments, 'form': form})


def questions(request):
    questions = Question.objects.all()
    return render(request, 'chats/quests.html', {'questions': questions})


# def search(request):
#     if request.method == 'POST':
#         search_result = request.POST['searched']
#         result = Question.objects.filter(Q(text__icontains=search_result) | Q(user__username__icontains=search_result))
#         return render(request, 'chats/index.html', {'questions': result})
#     else:
#         return render(request, 'chats/index.html')
def search(request):
    if request.method == 'POST':
        search_result = request.POST['searched']
        questions = Question.objects.filter(Q(text__icontains=search_result) | Q(user__username__icontains=search_result))
        comments = Comment.objects.filter(text__icontains=search_result)

        # Combine questions and comments into a single list
        result_list = list(questions) + list(comments)

        return render(request, 'chats/index.html', {'questions': result_list})
    else:
        return render(request, 'chats/index.html')


def like(request, pk):
    question = get_object_or_404(Question, id=pk)
    if request.user in question.like.all():
        question.like.remove(request.user)
    else:
        question.like.add(request.user)
    return HttpResponseRedirect('/')


def hashtag(request, hashtag):
    questions = Question.objects.filter(hashtag=hashtag)
    return render(request, 'chats/index.html', context={'questions': questions, 'hashtag': hashtag})

