from django.shortcuts import render, get_object_or_404

from .models import Question, Answer, Tag
from .utils import paginate

def index(request):
    questions = (
        Question.objects
        .select_related('user', 'user__profile')
        .prefetch_related('tags')
        .order_by('-creation_time')
    )

    page_obj = paginate(questions, request)

    return render(
        request,
        'questions/index.html',
        context={
            'page_obj': page_obj,
        }
    )

def hot(request):
    questions = (
        Question.objects
        .select_related('user', 'user__profile')
        .prefetch_related('tags')
        .order_by('-vote_count')
    )

    page_obj = paginate(questions, request)

    return render(
        request,
        'questions/hot.html',
        context={
            'page_obj': page_obj,
        }
        )


def ask(request):
    return render(
        request,
        'questions/ask.html',

        )

def question(request, question_id):
    question_obj = get_object_or_404(
        Question.objects
        .select_related('user', 'user__profile')
        .prefetch_related('tags')
        .filter(id=question_id)
    )

    answers = (
        Answer.objects
        .filter(question=question_obj)
        .select_related('user', 'user__profile')
        .order_by('-is_correct', '-vote_count', '-creation_time')
    )

    page_obj = paginate(answers, request)

    return render(
        request,
        'questions/question.html',
        context={
            'question': question_obj,
            'page_obj': page_obj,
        }
        )

def tag(request, tag_name):
    tag_obj = get_object_or_404(Tag, name=tag_name)

    questions = (
        Question.objects
        .filter(tags=tag_obj)
        .select_related('user', 'user__profile')
        .prefetch_related('tags')
        .order_by('-vote_count')
    )

    page_obj = paginate(questions, request)

    return render(
        request,
        'questions/tag.html',
        context={
            'page_obj': page_obj,
            'tag': tag_obj
        }
        )